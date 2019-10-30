from . import app
from blitz.root import get_logger

logger = get_logger()


@app.handle(domain='nfl', intent='get_depth_chart')
def get_depth_chart(request, responder):
    responder.reply("Here is the depth chart")


@app.handle(domain='nfl', intent='get_dvoa')
def get_dvoa(request, responder):
    responder.reply("Here is the dvoa")


@app.handle(domain='nfl', intent='get_injury_report')
def get_injury_report(request, responder):
    responder.reply("Here is the injury report")


@app.handle(domain='nfl', intent='get_trivia')
def get_trivia(request, responder):
    responder.reply("Here is the trivia")