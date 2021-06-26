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

    curmodule = None
    print(modules)
    for mo in modules:
        if args[0] == mo['command'] and mo['enabled']:
            curmodule = mo['filename']
            curlocation = mo['location']
            curmainfunc = mo['mainfunc']
            break

    if curmodule is not None:
        try:
            sys.path.insert(1, curlocation)
            loadmd = __import__(curmodule)
            func = getattr(loadmd, curmainfunc)
            await func(ctx, args)
        except Exception as e:
            await ctx.send("에러! 모듈 실행중 오류가 발생했습니다")
    else:
        ctx.send('에러! 명령어가 없습니다!')

bot.run(token)
