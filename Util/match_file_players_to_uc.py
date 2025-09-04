from src.Util.UCDatabase import UCDatabase
from src.Util.get_players import get_players


def match_file_players_to_uc(file_loc, fields):
    players_in_file = get_players(file_loc)

    database = UCDatabase("football_4")
    players_in_database = database.run_select("database_masterlist", fields, "`class` >= 2020")

    combined_data = []
    for row_data in players_in_file.items():
        player_id = row_data[0]

        match = None
        for database_player in players_in_database:
            if str(player_id) == str(database_player["Player ID"]):
                match = database_player
        if match is None:
            print("not found")
            continue

        match["College"] = row_data[1][0]
        combined_data.append(match)

    return combined_data
