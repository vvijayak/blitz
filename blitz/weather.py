# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain
in the MindMeld home assistant blueprint application
"""
from . import app
from .nfl.team import Team
from blitz.root import get_logger

logger = get_logger()


@app.handle(domain='weather', intent='check_weather')
def check_weather(request, responder):

    team = Team()
    for e in request.entities:
        if e['type'] == 'team':
            team = Team(team_name=e['value'][0]['cname'])

    temperature, city_name = team.current_weather
    responder.reply(f'Right now in {city_name} by {team.stadium_name} it is {temperature} degrees.')
