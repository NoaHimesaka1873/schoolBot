import discord
import os
import re
import food
from datetime import datetime, date, timedelta
from discord.ext import commands
from multiprocessing import Process, Pipe

bot = commands.Bot("학교봇 ")
token = ""
with open("discordtoken.txt", "r") as tk:
    token = re.sub('[\s+]', '', tk.read()).rstrip()

with open("neistoken.txt", "r") as tk:
    key = re.sub('[\s+]', '', tk.read()).rstrip()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="도움말을 보시려면 \"학교봇 도움말\"을 이용해주세요!"))


@bot.command(name="급식")
async def _sayFood(ctx, _date: str, school: str, foodtype: str):
    if _date == "오늘":
        _date = datetime.today().strftime('%Y%m%d')
    elif _date == "내일":
        _date = (date.today() + timedelta(days=1)).strftime('%Y%m%d')
    # os.system(f"python food.py {_date} {school} {foodtype}")

    #with open(f"{school} {_date} food.txt", "r") as f:
    #    foodie = f.read()
    #    await check(foodie, ctx)
    pipecon_p, pipecon_c = Pipe()
    p = Process(target=food.getfood, args=(foodtype, key, school, _date, pipecon_c,))
    p.start()
    foodie = pipecon_p.recv()
    p.join()
    await check(foodie, ctx)


@bot.command(name="학사일정")
async def _saySchedule(ctx, school: str):
    os.system("python schedule.py {}".format(school))
    with open(f"{school} {datetime.today().strftime('%Y%m%d')} schedule.txt") as f:
        schedule = f.read()
        await check(schedule, ctx)


@bot.command(name="도움말")
async def _help(ctx):
    with open("help.md", "r") as f:
        await ctx.send(f.read())


@bot.command(name="시간표")
async def _sayTimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    sctype = "his"
    if schtype == "초등학교":
        sctype = "els"
    elif schtype == "중학교":
        sctype = "mis"
    os.system(f"python timetable.py {school} {grade} {classnm} {sctype} 0")
    with open(f"{school} {datetime.today().strftime('%Y%m%d')} timetable.txt", "r") as f:
        timetable = f.read()
        await check(timetable, ctx)


@bot.command(name="특수시간표")
async def _saySpecialTimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    os.system(f"python timetable.py {school} {grade} {classnm} {schtype} 1")
    with open(f"{school} {datetime.today().strftime('%Y%m%d')} timetable.txt", "r") as f:
        timetable = f.read()
        await check(timetable, ctx)


async def check(chk: str, ctx):
    if not chk:
        await ctx.send("ERROR!")
    else:
        await ctx.send(chk)


bot.run(token)
