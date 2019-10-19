# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain
in the MindMeld home assistant blueprint application
"""
from . import app
from .nfl.team import Team
from sys import exit

team = Team()

@app.handle(domain='general', intent='greet')
def greet(request, responder):
    responder.reply('Hey {}, I\'m your person NFL Webex Asssistant Agent'.format(team.team_name))

@app.handle(domain='general', intent='exit')
def exit(request, responder):
    responder.reply('Hope I was helpful. Bye.'.format(team.team_name))
