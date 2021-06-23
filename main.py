import discord
import json
from discord.ext import commands
import sys

bot = commands.Bot("학교")
with open("settings.json", "r") as settings:
    token = json.load(settings)['discord_token']


@bot.event
async def on_ready():
    with open("settings.json", "r") as pre:
        await bot.change_presence(activity=discord.Game(name=json.load(pre)['presence']))


@bot.command(name="봇")
async def decodeCommand(ctx, *args):
    with open("modules.json") as _modules:
        modules = json.load(_modules)
    try:
        sys.path.insert(1, modules[args[0]]['location'])
        loadmd = __import__(modules[args[0]]['filename'])
        func = getattr(loadmd, modules[args[0]]['mainfunc'])
        await func(ctx, args)
    except Exception as e:
        await ctx.send("ERROR! 명령어가 없습니다.")
        print(e)

bot.run(token)
