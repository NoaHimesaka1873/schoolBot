import asyncio
import json
import nest_asyncio
from datetime import date
from datetime import datetime
from datetime import timedelta

import discord
from neispy import Neispy

ftr1 = ["", "조식", "중식", "석식"]
ftr2 = {"조식": 1, "중식": 2, "석식": 3, "all": 4}

with open("settings.json", "r") as settings:
    key = json.load(settings)["neis_token"]
neis = Neispy.sync(KEY=key)
nest_asyncio.apply()


def getfood(schoolname: str, _date: str, foodtype: int):
    try:
        schoolinfo = asyncio.new_event_loop().run_until_complete(
            neis.schoolInfo(SCHUL_NM=schoolname)
        )
        schoolmeal = asyncio.new_event_loop().run_until_complete(
            neis.mealServiceDietInfo(
                schoolinfo[0].ATPT_OFCDC_SC_CODE,
                schoolinfo[0].SD_SCHUL_CODE,
                MLSV_YMD=int(_date),
                MMEAL_SC_CODE=foodtype,
            )
        )
        return "\n".join(schoolmeal[0].DDISH_NM.split("<br/>"))
    except Exception as e:
        with open(f"{datetime.today().strftime('%c')} error.log", "a") as f:
            f.write(str(e))
        return None


def food2embed(schoolname, foodtype, foodie, _date):
    embed = discord.Embed(title=f"{schoolname}의 급식", color=discord.Color.blue())
    embed.add_field(
        name=f"{datetime.strptime(_date, '%Y%m%d').strftime('%Y년 %m월 %d일')} ({foodtype})",
        value=foodie,
    )
    return embed


async def main(ctx, args):
    if len(args) == 4:
        _foodtype = args[3]
    elif len(args) == 3:
        _foodtype = "all"
    else:
        await ctx.send("에러! 인자의 개수가 잘못되었습니다. 도움말을 참고해주세요.")
        return

    _date = args[1]
    school = args[2]

    if _date == "오늘":
        _date = datetime.today().strftime("%Y%m%d")
    elif _date == "내일":
        _date = (date.today() + timedelta(days=1)).strftime("%Y%m%d")

    foodtype = ftr2[_foodtype]

    if foodtype == 4:
        bldlist = []
        for i in range(1, 4):
            bldlist.append([getfood(school, _date, i), i])

        for foodie in bldlist:
            if foodie[0] is not None:
                embed = food2embed(school, ftr1[foodie[1]], foodie[0], _date)
                await ctx.send(embed=embed)

        if all(v[0] is None for v in bldlist):
            await ctx.send("에러! 데이터가 없습니다.")

    else:
        foodie = getfood(school, _date, foodtype)
        if foodie is not None:
            embed = food2embed(school, ftr1[foodtype], foodie, _date)
            await ctx.send(embed=embed)
        else:
            await ctx.send("에러! 데이터가 없습니다.")
