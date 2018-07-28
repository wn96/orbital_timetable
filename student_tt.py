from mods_lib import *
import constants

def expand_url(url): # expands nusmods url
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url

def mod_list_student(url): # return students schedule in dictionary format: {<modcode>: [(Classtype, no.)]...}
    def seg(url): # seperate modules from URL to elements in list
        mods = []
        while "?" in url:
            pos = url.index("?")
            url = url[pos+1:]
        while "&" in url:
            pos_am = url.index("&")
            mods.append(url[:pos_am])
            url = url[pos_am + 1:]
        mods.append(url)
        return mods

    expanded_url = expand_url(url) # Expands URL to show module taken
    mods = seg(expanded_url) # list of modules taken, seperated
    schedule = {}
    for mod in mods:
        tmp = mod.index("=")
        mod_code = mod[:tmp]
        mod = mod[tmp+1:]
        classes = []
        block=mod.split(",")
        for i in block:
            tmp2 = tuple((i.split(":")))
            classes.append(tmp2)
        schedule[mod_code] = classes
    return schedule

#Return the list of student classes' timeslot
def student_schedule(student_mods):
    schedule=[]
    for mod in student_mods.keys():
        mod_timetable = constants.NUS_MODULES[mod]
        for i in student_mods[mod]:
            if i in mod_timetable.keys():
                schedule.extend(mod_timetable[i])
    return schedule
