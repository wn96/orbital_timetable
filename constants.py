STARTTIME = "0600"
ENDTIME = "2200"

INTERVAL = 30

nus_modules.get_nus_modules_json() # update modules
NUS_MODULES = nus_modules.nusmod_list("modules.json")

TOKEN = "539235421:AAF_Ckn94vuRqG4EwPeUTLllFfneIVtMGeA"

WEEK_TODAY = 1
SEMESTER_HEADER = "AY2018/19, Semester 1"

SEMESTER_NO = 1

import importlib
if importlib.util.find_spec("selenium") is not None:
    import scrap_week
    WEEK = scrap_week.scrapper()
    if WEEK is not None:
        SEMESTER_HEADER, WEEK_TODAY = WEEK
        SEMESTER_NO = {"1": 1, "2": 2, "I": 3, "II": 4}\
            [SEMESTER_HEADER.split(" ")[-1]]
