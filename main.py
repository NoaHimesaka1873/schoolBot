import discord
from discord.ext import commands
import os
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
async def _sayfood(ctx, school: str):
    os.system("python food.py {} 1 1 0 his".format(school))
    f = open("food.txt", "r")
    foodie = f.read()
    if foodie is "":
        await ctx.send("ERROR!")
    else:
        await ctx.send(foodie)
    f.close()

@bot.command(pass_context=True, name="도움말")
async def _help(ctx):
    await ctx.send("학교봇 도움말:\n학교봇 급식 (학교명) : 오늘의 급식을 출력합니다. 데이터가 존재하지 않거나 잘못된 학교명을 입력했을 시에는 ERROR!가 출력됩니다.\n학교봇 시간표 (학교 종류) (학교명) (학년) (반) : 시간표를 출력합니다. 대부분의 경우에는 데이터가 없기 떄문에 ERROR!가 출력됩니다. 잘못된 입력 시에도 ERROR!가 출력됩니다.\n학교 종류: 초등학교 중학교 고등학교")

@bot.command(pass_context=True, name="시간표")
async def _saytimetable(ctx, schtype: str, school: str, grade: int, classnm: int):
    sctype = "his"
    if schtype == "초등학교":
        sctype = "els"
    elif schtype == "중학교":
        sctype = "mis"
    os.system("python food.py {} {} {} 1 {}".format(school, grade, classnm, sctype))
    f = open("timetable.txt", "r")
    timetable = f.read()
    if timetable is "":
        await ctx.send("ERROR!")
    else:
        await ctx.send(timetable)
    f.close()

bot.run(token)


