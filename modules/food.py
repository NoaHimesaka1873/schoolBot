import asyncio
import nest_asyncio
import neispy
import discord
import json
from datetime import datetime, date, timedelta

nest_asyncio.apply()

ftreference = ["", "조식", "중식", "석식"]

with open("settings.json", "r") as settings:
    key = json.load(settings)["neis_token"]


def getfood(schoolname: str, _date: str, foodtype: int):
    neis = neispy.Client(KEY=key)
    try:
        schoolinfo = asyncio.new_event_loop().run_until_complete(
            neis.schoolInfo(SCHUL_NM=schoolname)
        )
        AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
        SSC = schoolinfo[0].SD_SCHUL_CODE
        schoolmeal = asyncio.new_event_loop().run_until_complete(
            neis.mealServiceDietInfo(
                AOSC, SSC, MLSV_YMD=int(_date), MMEAL_SC_CODE=foodtype
            )
        )
        meal = "\n".join(schoolmeal[0].DDISH_NM.split("<br/>"))
        return meal
    except Exception as e:
        print(e)
        return None


async def main(ctx, args):
    _date = args[1]
    school = args[2]
    _foodtype = ""

    if len(args) == 4:
        _foodtype = args[3]
    else:
        _foodtype = "all"

    if _date == "오늘":
        _date = datetime.today().strftime("%Y%m%d")
    elif _date == "내일":
        _date = (date.today() + timedelta(days=1)).strftime("%Y%m%d")

    if _foodtype == "조식":
        foodtype = 1
    elif _foodtype == "중식":
        foodtype = 2
    elif _foodtype == "all":
        foodtype = 4
    else:
        foodtype = 3

    if foodtype == 4:
        breakfast = getfood(school, _date, 1)
        lunch = getfood(school, _date, 2)
        dinner = getfood(school, _date, 3)
        if breakfast is not None:
            embed1 = discord.Embed(title=f"{school}의 급식", color=discord.Color.blue())
            embed1.add_field(
                name=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')} ({ftreference[1]})",
                value=breakfast,
            )
            await ctx.send(embed=embed1)

        if lunch is not None:
            embed2 = discord.Embed(title=f"{school}의 급식", color=discord.Color.blue())
            embed2.add_field(
                name=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')} ({ftreference[2]})",
                value=lunch,
            )
            await ctx.send(embed=embed2)

        if dinner is not None:
            embed3 = discord.Embed(title=f"{school}의 급식", color=discord.Color.blue())
            embed3.add_field(
                name=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')} ({ftreference[3]})",
                value=dinner,
            )
            await ctx.send(embed=embed3)

    else:
        foodie = getfood(school, _date, foodtype)
        if foodie is not None:
            embed = discord.Embed(title=f"{school}의 급식", color=discord.Color.blue())
            embed.add_field(
                name=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')} ({ftreference[foodtype]})",
                value=foodie,
            )
            print("everything is done! ready to send")
            await ctx.send(embed=embed)
