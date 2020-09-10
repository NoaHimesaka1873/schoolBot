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

@bot.command(pass_context=True, name="급식")
async def _sayfood(ctx, school: str, foodtype: str):
    os.system("python food.py {} {}".format(school, foodtype))
    f = open("{} {} food.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    foodie = f.read()
    if foodie is "":
        await ctx.send("ERROR!")
    else:
        await ctx.send(foodie)
    f.close()

@bot.command(pass_context=True, name="학사일정")
async def _sayschedule(ctx, school: str):
    os.system("python schedule.py {}".format(school))
    f = open("{} {} schedule.txt".format(school, datetime.today().strftime("%Y%m%d")))
    schedule = f.read()
    if schedule == "":
        await ctx.send("ERROR!")
    else:
        await ctx.send(schedule)
    f.close()

@bot.command(pass_context=True, name="도움말")
async def _help(ctx):
    f = open("help.md", "r")
    await ctx.send(f.read())
    f.close()

@bot.command(pass_context=True, name="시간표")
async def _saytimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    sctype = "his"
    if schtype == "초등학교":
        sctype = "els"
    elif schtype == "중학교":
        sctype = "mis"
    os.system("python timetable.py {} {} {} {} 0".format(school, grade, classnm, sctype))
    f = open("{} {} timetable.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    timetable = f.read()
    if timetable is "":
        await ctx.send("ERROR!")
    else:
        await ctx.send(timetable)
    f.close()

@bot.command(pass_context=True, name="특수시간표")
async def _sayspecialtimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    #os.system("python timetable.py {} {} {} {} 1".format(school, grade, classnm, schtype))
    #f = open("{} {} timetable.txt".format(school, datetime.today().strftime("%Y%m%d")), "r")
    #timetable = f.read()
    #if timetable is "":
    #    await ctx.send("ERROR!")
    #else:
    #    await ctx.send(timetable)
    #f.close()
    ## 현재 neispy의 특수학교 학교급구분 미지원으로 사용 불가.
    await ctx.send("현재 이 기능은 API Wrapper와 관련된 문제로 인하여 사용이 불가능합니다. 후에 기능이 지원되면 활성화 예정입니다.")

bot.run(token)


