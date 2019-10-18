import json


class Team:

    def __init__(self, team_name):

        self.JSON_FILE = "blitz/nfl/teams.json"
        self.team_name = team_name

    @property
    def depth_chart_defense(self):
        return self.team_json['depth_chart']['offense']

    @property
    def depth_chart_offense(self):
        return self.team_json['depth_chart']['offense']

    @property
    def depth_chart_special(self):
        return self.team_json['depth_chart']['special']

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