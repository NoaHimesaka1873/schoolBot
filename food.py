import neispy
import sys
import re
import json

with open("neistoken.txt", "r") as tk:
    key = re.sub('[\s+]', '', tk.read()).rstrip()

isDinner = False
isBreakfast = False
schoolname = sys.argv[2]
foodtype = sys.argv[3]
_date = sys.argv[1]
if foodtype == "석식":
    isDinner = True
if foodtype == "조식":
    isBreakfast = True


def getfood():
    neis = neispy.Client(KEY=key)

    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE
    if isDinner:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(_date),
                                              MMEAL_SC_CODE=3)
    elif isBreakfast:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(_date),
                                              MMEAL_SC_CODE=1)
    else:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(_date))
    meal = schoolmeal[0].DDISH_NM.split("<br/>")
    return meal


_meal = getfood()
with open(f"{schoolname} {_date} food.json", "w+") as f:
    json.dump(_meal, f)
