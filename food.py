import neispy
import sys
import re

#with open("neistoken.txt", "r") as tk:
#    key = re.sub('[\s+]', '', tk.read()).rstrip()

#isDinner = False
#isBreakfast = False
#schoolname = sys.argv[2]
#_foodtype = sys.argv[3]
#_date = sys.argv[1]



def getfood(foodtype: str, key: str, schoolname: str, _date: str, conn):
    if foodtype == "석식":
        isDinner = True
    if foodtype == "조식":
        isBreakfast = True
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
    meal = schoolmeal[0].DDISH_NM.replace("<br/>", "\n")
    print(schoolmeal[0].MMEAL_SC_CODE)
    conn.send(meal)
    conn.close()


if __name__ == '__main__':
    _meal = getfood(_foodtype)
    with open(f"{schoolname} {_date} food.txt", "w+") as f:
        f.write(_meal)
