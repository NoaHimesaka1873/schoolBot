import json
import neispy
import re
import sys
from datetime import datetime

with open("neistoken.txt", "r") as tk:
    key = re.sub('[\s+]', '', tk.read()).rstrip()

schoolname = sys.argv[1]
grade = int(sys.argv[2])
_class = int(sys.argv[3])
schtype = sys.argv[4]
isSpecial = int(sys.argv[5])


def gettimetable():
    neis = neispy.Client(KEY=key)
    sctimetable = None
    schoolinfo = neis.schoolInfo(SCHUL_NM=schoolname)
    AOSC = schoolinfo[0].ATPT_OFCDC_SC_CODE
    SSC = schoolinfo[0].SD_SCHUL_CODE
    if isSpecial:
        sctimetable = neis.timeTable(schclass="sps", ATPT_OFCDC_SC_CODE=AOSC, SD_SCHUL_CODE=SSC,
                                     ALL_TI_YMD=int(datetime.today().strftime("%Y%m%d")), GRADE=grade, CLASS_NM=_class,
                                     SCHUL_CRSE_SC_NM=schtype)
    else:
        sctimetable = neis.timeTable(schclass=schtype, ATPT_OFCDC_SC_CODE=AOSC, SD_SCHUL_CODE=SSC,
                                     ALL_TI_YMD=int(datetime.today().strftime("%Y%m%d")), GRADE=grade, CLASS_NM=_class)
    timetable = [i.ITRT_CNTNT for i in sctimetable]
    return timetable


_timetable = gettimetable()
with open(f"{schoolname} {datetime.today().strftime('%Y%m%d')} timetable.json", "w+") as f:
    json.dump(_timetable, f)
