from blitz.root import NFL_DATA_PATH
import json


class Team:

    def __init__(self):

        self.JSON_FILE = f'{NFL_DATA_PATH}/league.json'

        with open(self.JSON_FILE) as json_file:
            league_data = json.load(json_file)
