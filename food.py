import neispy
import sys
from datetime import datetime


tk = open("neistoken.txt", "r")
isDinner = False
key = tk.read()
tk.close()
schoolname = sys.argv[1]
foodtype = sys.argv[2]
if foodtype == "석식":
    isDinner = True

def getfood():
    neis = neispy.Client(KEY=key)

    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE
    if isDinner:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")), MMEAL_SC_CODE=3)
    else:
        schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")))
    meal = schoolmeal[0].DDISH_NM.replace("<br/>", "\n")
    print(schoolmeal[0].MMEAL_SC_CODE)
    return meal


_meal = getfood()
f = open("{} {} food.txt".format(schoolname, datetime.today().strftime("%Y%m%d")), "w+")
f.write(_meal)

f.close()
