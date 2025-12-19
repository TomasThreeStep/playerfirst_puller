import json

import requests

from Util.UCDatabase import UCDatabase


def login(username,password):
	resp = requests.post(
		"https://playerfirst-staging.azurewebsites.net/api/auth",
		json={
			"username": username,
			"password": password
		}
	)

	resp_json = resp.json()

	return resp_json


def get_programs(affiliationId):

	vowels = ["a", "e", "i", "o", "u"]

	all_programs = []
	for vowel in vowels:
		resp = requests.get(
			f"https://playerfirst-staging.azurewebsites.net/api/suggest/program?affiliationId={str(affiliationId)}&q={vowel}&pastVisible=true&limit=100&approvedOnly=false"
		)
		vals = resp.json()
		all_programs = all_programs + vals

	seen = set()
	unique = []
	for item in all_programs:
		if item['name'] not in seen:
			unique.append(item)
			seen.add(item['name'])

	return unique


def get_program_info(program,aff,jwt):

	resp = requests.get(
		# f"https://playerfirst-staging.azurewebsites.net/api/program/{program["value"]}/division"
		f"https://playerfirst-staging.azurewebsites.net/api/suggest/division?programId={program["value"]}&limit=90000&affiliationId={aff}&isRegistrationByTeamOnly=false&showProgram=false&showBrand=false",
		# f"https://playerfirst-staging.azurewebsites.net/api/suggest/division?programId=15601&limit=90000&affiliationId=156&isRegistrationByTeamOnly=false&showProgram=false&showBrand=false",
		headers={"Authorization": f"Bearer {jwt}"}
	)
	resp_json = resp.json()

	return resp_json


def get_roster(division,jwt):
	resp = requests.get(
		f"https://playerfirst-staging.azurewebsites.net/api/roster/division/{division["value"]}",
		headers={"Authorization": f"Bearer {jwt}"}
	)
	resp_json = resp.json()['roster']

	return resp_json

def insert_affiliation(affil):

	query = f"""
	INSERT INTO football_test.database_playerfirstaffiliation
	    (Dbkey, Name, id)
	    VALUES(0, '{affil["name"]}', {affil["id"]});
	"""
	database.run_query(query)
	return None

def insert_program(program,id):

	name = program["name"]

	program_aff_db = database.run_select("database_playerfirstaffiliation",["Dbkey"], f" `id` = '{id}' ")[0]["Dbkey"]


	query = f"""
	INSERT INTO football_test.database_playerfirstprogram
	    (Dbkey, Name, AffiliationID,prog_id)
	    VALUES(0, '{name}', {program_aff_db}, {str(program["value"])});
	"""
	database.run_query(query)
	program = database.run_select("database_playerfirstprogram",["Dbkey"], f" `name` = '{name}' ")[0]["Dbkey"]
	return program

def insert_division(name,program):
	query = f"""
	INSERT INTO football_test.database_playerfirstdivision
	    (Dbkey, Name, programID)
	    VALUES(0, "{name}", {program});
	"""
	database.run_query(query)
	division = database.run_select("database_playerfirstdivision",["Dbkey"], f" `name` = '{name}' AND `programID` = {program} ")[0]["Dbkey"]
	return division


def insert_roster(name,roster,division):
	roster_str = json.dumps(roster, indent=4).replace("'", "\\'")
	# print(roster_str)


	query = f"""
	INSERT INTO football_test.database_playerfirstrosters
	    (Dbkey, Name, `Data`, DivisionID, RosterCount)
	    VALUES(0, '{name}', '{roster_str}', {division}, {len(roster)});
	"""
	database.run_query(query)

def insert_prospect(player):
	pass




username = "ucreport@threestep.com"
password = "Persona487"

database = UCDatabase("football_test")

def main():

	database.run_query(f"""DELETE FROM football_test.database_playerfirstrosters;""")
	database.run_query(f"""DELETE FROM football_test.database_playerfirstdivision;""")
	database.run_query(f"""DELETE FROM football_test.database_playerfirstprogram;""")
	database.run_query(f"""DELETE FROM football_test.database_playerfirstaffiliation;""")

	resp_json = login(username,password)
	affiliations = resp_json['affiliations']
	jwt = resp_json['jwt']

	for affiliation in resp_json["affiliationDetails"]:
		insert_affiliation(affiliation)


	for affiliation in affiliations:

		# if affiliation != 156:
		# 	continue

		programs = get_programs(affiliation)

		try:
			for program in programs:
				program_info = get_program_info(program,affiliation,jwt)

				prog = insert_program(program,affiliation)

				try:

					print(program["name"])
					for division in program_info:
						# if division["name"] != "Player Registration - Central Florida - 8U":
						# 	continue

						name_to_insert = division['name']
						# name_to_insert = division['name']
						div = insert_division(name_to_insert,prog)

						print("\t\t"+division["name"])

						if division["name"] == "deprecated":
							continue
						try:
							roster = get_roster(division,jwt)

							insert_roster(division["name"],roster,div)
						except Exception as e:
							print(e)
							# raise e
				except Exception as e:
					print(e)

		except Exception as e:
			print(e)
			# print(divisions)

		print(resp_json)





if __name__ == "__main__":
	main()