from blitz.root import get_logger, NFL_DATA_PATH
import json


import requests

API_KEY = '02a4a31db6c0092319a615aa55eadb3a'
CURRENT_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

logger = get_logger()


class Team:

    def __init__(self, team_name="Seahawks"):

        self.JSON_FILE = f'{NFL_DATA_PATH}/teams.json'
        self.team_name = team_name

        try:
            data = None
            with open(self.JSON_FILE) as json_file:
                data = json.load(json_file)
                team_json = data[team_name]

            self.depth_chart_defense = f"{team_json['domain']}/team/depth-chart#scroll-defense"
            self.depth_chart_offense = f"{team_json['domain']}/team/depth-chart#scroll-offense"
            self.depth_chart_special = f"{team_json['domain']}/team/depth-chart#scroll-specialteams"
            self.injury_report = f"{team_json['domain']}/team/depth-chart#scroll-specialteams"
            self.news = f"{team_json['domain']}/team/injury-report/"
            self.stadium_name = team_json['stadium']['name']
            self.stadium_zip_code = team_json['stadium']['zip_code']
            self.transactions = f"{team_json['domain']}team/transactions/"

        except Exception as e:
            logger.error(e)
            pass

    @property
    def current_weather(self):

        params = {'zip': f'{self.stadium_zip_code},us', 'appid': API_KEY, 'units': 'imperial'}
        try:
            response = requests.get(
                url=CURRENT_WEATHER_API,
                params=params
            )
        except Exception as e:
            logger.error(e)
            return None
        weather = response.json()
        return int(weather['main']['temp']), weather['name']

