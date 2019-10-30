from . import app
from blitz.root import get_logger
from .nfl.team import Team
import requests
import lxml.html as lh
from collections import defaultdict
import json
from blitz.root import NFL_DATA_PATH
import pandas as pd
import re


logger = get_logger()

CANONICAL_NAME_TO_ABBRVIATION = {
    "49ers": "SF",
    "Bears": "CHI",
    "Bengals": "CIN",
    "Bills": "BUF",
    "Broncos": "DEN",
    "Browns": "CLE",
    "Buccaneers": "TB",
    "Cardinals": "ARI",
    "Chargers": "LAC",
    "Chiefs": "KC",
    "Colts": "IND",
    "Cowboys": "DAL",
    "Dolphins": "MIA",
    "Eagles": "PHI",
    "Falcons": "ATL",
    "Giants": "NYG",
    "Jaguars": "JAX",
    "Jets": "NYJ",
    "Lions": "DET",
    "Packers": "GB",
    "Panthers": "CAR",
    "Patriots": "NE",
    "Raiders": "OAK",
    "Rams": "LAR",
    "Ravens": "BAL",
    "Redskins": "WAS",
    "Saints": "NO",
    "Seahawks": "SEA",
    "Steelers": "PIT",
    "Texans": "HOU",
    "Titans": "TEN",
    "Vikings": "MIN",
}


@app.handle(domain='nfl', intent='get_depth_chart')
def get_depth_chart(request, responder):
    team_entities = [x for x in request.entities if x['type'] == 'team']
    canonical_team_name = team_entities[0]['value'][0]['cname']
    team_object = Team(team_name=canonical_team_name)

    page = requests.get(team_object.depth_chart_offense)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')

    position_to_players = defaultdict(list)

    for element in tr_elements:
        element_children = element.getchildren()
        position = element_children[0].text_content().lstrip().rstrip()

        if position != 'Position':
            for e in element_children[1:]:
                player = e.text_content().lstrip().rstrip()
                if player:
                    position_to_players[position].append(player)

    position_entity = [x for x in request.entities if x['type'] == 'position']
    if position_entity:
        position = position_entity[0]['value'][0]['cname']
        players_at_position = position_to_players[position]

        responder.reply(f"Here is the {position} depth chart for the {canonical_team_name}:")
        responder.reply(", ".join(players_at_position))
    else:
        responder.frame['position_to_players_dict'] = position_to_players
        responder.frame['requested_team'] = canonical_team_name
        responder.reply(f"Which position would you like to see for the {canonical_team_name}?")


@app.handle(domain='nfl', intent='specify_position')
def specify_position(request, responder):
    position_entity = [x for x in request.entities if x['type'] == 'position']
    if position_entity:
        position_to_players = responder.frame['position_to_players_dict']
        canonical_team_name = responder.frame['requested_team']

        position = position_entity[0]['value'][0]['cname']
        players_at_position = position_to_players[position]

        responder.reply(f"Here is the {position} depth chart for the {canonical_team_name}:")
        responder.reply(", ".join(players_at_position))
    else:
        responder.reply("Sorry, I didn't catch that. Which position would you like to see?")


@app.handle(domain='nfl', intent='get_dvoa')
def get_dvoa(request, responder):
    dvoa_json_file = f'{NFL_DATA_PATH}/league.json'
    with open(dvoa_json_file) as json_file:
        league_dvoa_data = json.load(json_file)

    dvoa_type_entity = [x for x in request.entities if x['type'] == 'dvoa_type']
    dvoa_type = dvoa_type_entity[0]['value'][0]['cname']

    if dvoa_type == "Offensive":
        dvoa_link = league_dvoa_data['DVOA']['offense']
        dvoa_column = "OFFENSEDVOA"
    elif dvoa_type == "Defensive":
        dvoa_link = league_dvoa_data['DVOA']['defense']
        dvoa_column = "DEFENSEDVOA"
    elif dvoa_type == "Overall":
        dvoa_link = league_dvoa_data['DVOA']['overall']
        dvoa_column = "TOTALDVOA"
    else:
        dvoa_link = league_dvoa_data['DVOA']['special']
        dvoa_column = "S.T.DVOA"

    page = requests.get(dvoa_link)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')

    columns = []
    for t in tr_elements[0]:
        name = re.sub(r"[\n\t\s]*", "", t.text_content().strip())
        columns.append((name, []))

    for t in tr_elements[1:]:
        children = t.getchildren()
        for i, c in enumerate(children):
            data = c.text_content().lstrip().rstrip()
            try:
                data = float(data)
            except:
                pass

            columns[i][1].append(data)

    dvoa_dict = {title:column for (title,column) in columns}
    dvoa_df = pd.DataFrame(dvoa_dict)

    team_entities = [x for x in request.entities if x['type'] == 'team']
    canonical_team_name = team_entities[0]['value'][0]['cname']

    team_abbreviation = CANONICAL_NAME_TO_ABBRVIATION[canonical_team_name]

    dvoa_value = dvoa_df[dvoa_df['TEAM'] == team_abbreviation][dvoa_column].iloc[0]
    responder.reply(f"The {canonical_team_name} {dvoa_type.lower()} DVOA is {dvoa_value}")


@app.handle(domain='nfl', intent='get_injury_report')
def get_injury_report(request, responder):
    team_entities = [x for x in request.entities if x['type'] == 'team']
    canonical_team_name = team_entities[0]['value'][0]['cname']
    team_object = Team(team_name=canonical_team_name)

    page = requests.get(team_object.injury_report)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')

    players_on_report = []

    # Skip first header line
    for line in tr_elements[1:]:
        player = line.getchildren()[0].text_content().lstrip().rstrip()
        # Two teams on each injury report page, other team starts with another header line
        if player == 'Player':
            break
        else:
            players_on_report.append(player)

    responder.reply(f"Here are the players on the {canonical_team_name} injury report:")
    responder.reply(", ".join(players_on_report))


@app.handle(domain='nfl', intent='get_trivia')
def get_trivia(request, responder):
    responder.reply("Here is the trivia")