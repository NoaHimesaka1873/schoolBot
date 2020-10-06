import discord
from discord.ext import commands
import os
from datetime import datetime

bot = commands.Bot("학교봇 ")
tk = open("discordtoken.txt", "r")
token = tk.read()
tk.close()
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="도움말을 보시려면 \"학교봇 도움말\"을 이용해주세요!"))

@bot.command(name="급식")
async def _sayfood(ctx, school: str, foodtype: str):
    os.system("python food.py {} {}".format(school, foodtype))
    f = open("{} {} food.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    foodie = f.read()
    await check(foodie, ctx)
    f.close()

@bot.command(name="학사일정")
async def _sayschedule(ctx, school: str):
    os.system("python schedule.py {}".format(school))
    f = open("{} {} schedule.txt".format(school, datetime.today().strftime("%Y%m%d")))
    schedule = f.read()
    await check(schedule, ctx)
    f.close()

@bot.command(name="도움말")
async def _help(ctx):
    f = open("help.md", "r")
    await ctx.send(f.read())
    f.close()

@bot.command(name="시간표")
async def _saytimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    sctype = "his"
    if schtype == "초등학교":
        sctype = "els"
    elif schtype == "중학교":
        sctype = "mis"
    os.system("python timetable.py {} {} {} {} 0".format(school, grade, classnm, sctype))
    f = open("{} {} timetable.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    timetable = f.read()
    await check(timetable, ctx)
    f.close()

@bot.command(name="특수시간표")
async def _sayspecialtimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    os.system("python timetable.py {} {} {} {} 1".format(school, grade, classnm, schtype))
    f = open("{} {} timetable.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    timetable = f.read()
    await check(timetable, ctx)
    f.close()

async def check(check: str, ctx):
    if not check:
        await ctx.send("ERROR!")
    else:
        await ctx.send(check)

bot.run(token)


