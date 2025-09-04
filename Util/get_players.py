import csv


def get_players(file):
    uc_player_file = open(file)
    reader = csv.DictReader(uc_player_file)

    good_player_offers = []
    for player_data in reader:
        if float(player_data['confidence']) >= 4:
            good_player_offers.append(player_data)
        else:
            print(player_data)

    players_by_offers = {}
    for player_data in good_player_offers:
        id = player_data["match"]

        if id not in players_by_offers:
            players_by_offers[id] = [player_data["offer"]]
        else:
            players_by_offers[id].append(player_data["offer"])

    return players_by_offers

