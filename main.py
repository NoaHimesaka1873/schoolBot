import discord
import os
import re
import json
from datetime import datetime, date, timedelta
from discord.ext import commands

bot = commands.Bot("학교봇 ")
token = ""
with open("discordtoken.txt", "r") as tk:
    token = re.sub('[\s+]', '', tk.read()).rstrip()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="도움말을 보시려면 \"학교봇 도움말\"을 이용해주세요!"))


@bot.command(name="급식")
async def _sayFood(ctx, _date: str, school: str, foodtype: str):
    if _date == "오늘":
        _date = datetime.today().strftime('%Y%m%d')
    elif _date == "내일":
        _date = (date.today() + timedelta(days=1)).strftime('%Y%m%d')
    os.system(f"python food.py {_date} {school} {foodtype}")
    with open(f"{school} {_date} food.json", "r") as f:
        foodie = '\n'.join(json.load(f))
        embed = discord.Embed(
            title=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')}의 급식",
            color=discord.Color.blue()
        )
        embed.add_field(name=f"{school} ({foodtype})", value=foodie)
        await ctx.send(embed=embed)


@bot.command(name="학사일정")
async def _saySchedule(ctx, school: str):
    os.system("python schedule.py {}".format(school))
    with open(f"{school} {datetime.today().strftime('%Y%m%d')} schedule.txt") as f:
        schedule = f.read()
        await check(schedule, ctx)


@bot.command(name="도움말")
async def _help(ctx):
    with open("help.json") as json_file:
        data = json.load(json_file)
        embed1 = discord.Embed(
            title="학교봇 도움말: 명령어",
            color=discord.Color.blue()
        )
        embed2 = discord.Embed(
            title="학교봇 도움말: 예시와 참고 사항",
            color=discord.Color.blue()
        )
        for i in data['commands']:
            embed1.add_field(name=i['command'], value=i['description'], inline=False)
        embed2.add_field(name="예시", value=data['examples'])
        embed2.add_field(name="참고 사항", value=data['instructions'])
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)


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
        await ctx.send("에러! 올바르지 않은 응답이 반환되었습니다.")
    else:
        await ctx.send(chk)


bot.run(token)
