import json


class Team:

    def __init__(self):

        self.JSON_FILE = "blitz/nfl/league.json"


    @property
    def news(self):
        return self.team_json['news']

    @property
    def stadium_zip_code(self):
        return self.team_json['zip_code']

    @property
    def team_json(self):
        data = None
        with open(self.JSON_FILE) as json_file:
            data = json.load(json_file)
        return data[self.team_name]

    @property
    def transactions(self):
        return self.team_json['transactions']