from . import app
from blitz.root import get_logger
from .nfl.team import Team
import requests
import lxml.html as lh
from collections import defaultdict


logger = get_logger()


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
    responder.reply("Here is the dvoa")


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