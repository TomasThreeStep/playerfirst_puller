
class TwoFourSevenPlayer:
    def __init__(self):
        self.player_id = ""
        self.first = ""
        self.last = ""
        self.state = ""
        self.player_class = ""
        self.position = ""
        self.link = ""
        self.high_school = ""
        self.signed = ""

    def populate(self,data):
        self.player_id = data["Player id"]
        self.first = data["First"]
        self.last = data["Last"]
        self.state = data["State"]
        self.player_class = data["Class"]
        self.position = data["Position Played"]
        self.link = data["Detail Link"]
        self.high_school = data["High School"]
