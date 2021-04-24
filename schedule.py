import neispy
import re
import sys
from datetime import datetime

with open("neistoken.txt", "r") as tk:
    key = re.sub('[\s+]', '', tk.read()).rstrip()

schoolname = sys.argv[1]


def getschedule():
    neis = neispy.Client(KEY=key)

    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE

    scschedule = neis.SchoolSchedule(ATPT_OFCDC_SC_CODE=AOSC, SD_SCHUL_CODE=SSC,
                                     AA_YMD=int(datetime.today().strftime("%Y%m%d")))
    schedule = scschedule[0].EVENT_NM
    return schedule


_schedule = getschedule()
with open(f"{schoolname} {datetime.today().strftime('%Y%m%d')} schedule.txt", "w+") as f:
    f.write(_schedule)
