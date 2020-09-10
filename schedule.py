import neispy
import sys
from datetime import datetime


tk = open("neistoken.txt", "r")
key = tk.read()
tk.close()
schoolname = sys.argv[1]
def getschedule():
    neis = neispy.Client(KEY=key)

    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE

    scschedule = neis.SchoolSchedule(ATPT_OFCDC_SC_CODE=AOSC, SD_SCHUL_CODE=SSC, AA_YMD=int(datetime.today().strftime("%Y%m%d")))
    schedule = scschedule[0].EVENT_NM 
    return schedule


_schedule = getschedule()
f = open("{} {} schedule.txt".format(schoolname, datetime.today().strftime("%Y%m%d")), "w+")
f.write(_schedule)
f.close()