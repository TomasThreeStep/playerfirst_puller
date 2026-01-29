import json

import requests

from Util.UCDatabase import UCDatabase


def login(username,password):
	resp = requests.post(
		"https://playerfirsttech.com/api/auth",
		json={
			"username": username,
			"password": password
		}
	)

	resp_json = resp.json()

	return resp_json


def get_programs(affiliation):

	vowels = ["a", "e", "i", "o", "u"]

	all_programs = []
	for vowel in vowels:
		resp = requests.get(
			f"https://playerfirsttech.com/api/suggest/program?affiliationId={str(affiliation["id"])}&q={vowel}&pastVisible=true&limit=100&approvedOnly=false"
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
		# f"https://playerfirsttech.com/api/program/{program["value"]}/division"
		f"https://playerfirsttech.com/api/suggest/division?programId={program["value"]}&limit=90000&affiliationId={aff}&isRegistrationByTeamOnly=false&showProgram=false&showBrand=false",
		# f"https://playerfirsttech.com/api/suggest/division?programId=15601&limit=90000&affiliationId=156&isRegistrationByTeamOnly=false&showProgram=false&showBrand=false",
		headers={"Authorization": f"Bearer {jwt}"}
	)
	resp_json = resp.json()

	return resp_json


def get_roster(division,jwt,program):
	resp = requests.get(
		f"https://playerfirsttech.com/api/roster/division/{division["value"]}",
		headers={"Authorization": f"Bearer {jwt}"}
	)
	resp_json = resp.json()['roster']


	test_resp = requests.post(
		f"https://www.ucfootballcamps.com/util/admin/Programs/default.aspx/UpdatePlayerGridTableData",
		headers={"Cookie": f"AffiliationId=373; DeviceToken=6c36b31be5add1a5f4ca30d8cb6f817eb6c2da8a1d95c667ffcd0effa6971aae; UserId=2341220; _ga_HH0G5J868B=GS2.1.s1768920925$o6$g1$t1768920959$j26$l0$h0; _ga=GA1.1.1766980624.1767022906; BodyClass=; NumberInCart=; UtcLastActive=1/20/2026 2:56:11 PM; jwtPermissions=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZXJtczIiOnsicm9sZUlkVG9BZmZpbGlhdGlvbklkcyI6eyIyIjpbNzEsODQsMTU2LDE4MSwxODksMjQ5LDM3M119fSwiYWZmaWxpYXRpb25pZCI6MzczLCJ1c2VyaWQiOjIzNDEyMjAsImFjY2Vzc0NvZGVJZCI6bnVsbCwidXNlcm5hbWUiOiJ1Y3JlcG9ydGFkbWluIiwicHJvZmlsZWlkcyI6bnVsbCwicmVhZG9ubHkiOmZhbHNlLCJnZHJpdmVhdXRoIjpudWxsLCJmaXJzdE5hbWUiOiJVQyIsInByb2ZpbGVJbWFnZVVybCI6bnVsbCwidGltZXpvbmVJZCI6IkVhc3Rlcm4gU3RhbmRhcmQgVGltZSIsImlzTWZhUmVxdWlyZWQiOnRydWUsImlzUGVyc2lzdGVudCI6ZmFsc2UsInByb2dyYW1JZCI6bnVsbCwiaXNzdWVkVXRjIjoiMjAyNi0wMS0yMFQxNDo1NTo0Ny4xNTU4Mzg5WiIsImV4cCI6MTc2OTUyNTc0N30.5CJJJq18NbM-lKibyOPw35ptdFQCsDdguETAYmluxPE"},
		json={"editMode":False,"programId":program,"divisionIds":[division["value"]]}

	)
	test_data = test_resp.json()["d"]["Data"]
	ret_val = []
	for row in test_data:
		new_row = {}
		for col in row["Data"]:
			new_row[col["k"]] = col["v"]
		ret_val.append(new_row)

	return ret_val

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

	uc_camps = None
	for affiliation in resp_json["affiliationDetails"]:
		if affiliation["name"] == "UC Football Camps":
			uc_camps = affiliation

	insert_affiliation(uc_camps)



	# if affiliation != 156:
	# 	continue

	programs = get_programs(uc_camps)

	# try:
	for program in programs:
		program_info = get_program_info(program,uc_camps,jwt)

		prog = insert_program(program,uc_camps["id"])

		# try:

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

			roster = get_roster(division,jwt,prog)

			insert_roster(division["name"],roster,div)
			# except Exception as e:
			# 	print(e)
				# raise e
		# except Exception as e:
		# 	print(e)

	# except Exception as e:
	# 	print(e)
		# print(divisions)

	print(resp_json)





if __name__ == "__main__":
	main()