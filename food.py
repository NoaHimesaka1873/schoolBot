import neispy
import sys
from datetime import datetime

with open("neistoken.txt", "r") as tk:
    key = tk.read()

isDinner = False
isBreakfast = False
schoolname = sys.argv[1]
foodtype = sys.argv[2]
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
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")),
                                              MMEAL_SC_CODE=3)
    elif isBreakfast:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")),
                                              MMEAL_SC_CODE=1)
    else:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")))
    meal = schoolmeal[0].DDISH_NM.replace("<br/>", "\n")
    print(schoolmeal[0].MMEAL_SC_CODE)
    return meal


_meal = getfood()
with open(f"{schoolname} {datetime.today().strftime('%Y%m%d')} food.txt", "w+") as f:
    f.write(_meal)
