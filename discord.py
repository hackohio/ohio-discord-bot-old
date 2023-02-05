from nextcord.ext import commands
import util

_bot = commands.Bot()

def start():
    _bot.run(util.config['discord']['token'])

