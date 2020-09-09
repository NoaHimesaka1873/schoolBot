import neispy
import sys
from datetime import datetime
f = open("food.txt", "w+")
f2 = open("timetable.txt", "w+")
tk = open("neistoken.txt", "r")
key = tk.read()
tk.close()
schoolname = sys.argv[1]
grade = int(sys.argv[2])
_class = int(sys.argv[3])
isTimetable = int(sys.argv[4])
schtype = sys.argv[5]
print("{} {} {}".format(grade, _class, isTimetable))
def getfood():
    neis = neispy.Client(KEY=key)

    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE

    schoolmeal = neis.mealServiceDietInfo(AOSC, SSC, MLSV_YMD=int(datetime.today().strftime("%Y%m%d")))
    meal = schoolmeal[0].DDISH_NM.replace("<br/>", "\n")
    if isTimetable:
        sctimetable = neis.timeTable(schclass=schtype, ATPT_OFCDC_SC_CODE=AOSC, SD_SCHUL_CODE=SSC, ALL_TI_YMD=int(datetime.today().strftime("%Y%m%d")), GRADE=grade, CLASS_NM=_class)
        timetable = str([i.ITRT_CNTNT for i in sctimetable])
    else:
        timetable = ""
    return meal, timetable

print(getfood())
_meal, _timetable = getfood()
f.write(_meal)
f2.write(_timetable)
f.close()
f2.close()