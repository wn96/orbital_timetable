from mods_lib import *

STARTTIME = constants.STARTTIME
ENDTIME = constants.ENDTIME
INTERVAL = constants.INTERVAL
NUS_MODULES = constants.NUS_MODULES

WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def get_freetime(url, week):
    '''returns dictionary of [odd/even][day][time] of when student is free,
        in boolean'''
    return free_time(student_schedule(mod_list_student(url)), week)


def blank_schedule():
    '''returns dictionary of [day][time] == True'''
    tmp = {}
    for day in WEEK:
        time = []
        timing = STARTTIME
        timeslot = time_diff(STARTTIME, ENDTIME)
        for min30 in range(timeslot):
            time.append(timing)
            timing = increase(timing, INTERVAL)
        tmp[day] = dict(map(lambda x: (x, True), time))
    return tmp


def free_time(events, week_no):
    '''Determines the free time of a student.
    dict format of [weeknum][day][time],...]'''
    result = blank_schedule()
    for event in events:
        week_num = event["WeekText"]  # [1,3,5,7,9,11,13] if odd week
        if week_no in week_num:
            day = event["DayText"]  # Monday, Tuesday, ....
            start = event["StartTime"]  # 24H format
            end = event["EndTime"]  # 24H format
            while time_inbetween(STARTTIME, ENDTIME, end) and time_inbetween(
                    STARTTIME, ENDTIME, start) and start < end:
                result[day][start] = False
                start = increase(start, INTERVAL)
    return result


def compare_tt(sch1, sch2):
    if sch1 is None:
        return sch2
    '''Compares between 2 schedule, and returns when
        they are mutually free'''
    result = sch1
    for day in WEEK:
        for time in result[day]:
            if sch2[day][time] == False:
                result[day][time] = False
    return result


def time_inbetween(start, end, time):
    return int(time) <= int(end) and int(start) <= int(time)


def viewer(schedule):
    timing = list(schedule[WEEK[0]].keys())
    weekevents = []
    for day in WEEK:
        dayevents = []
        for time in timing:
            if schedule[day][time] == True:
                dayevents.append(str(time))
        weekevents.append(dayevents)
    return weekevents


def view_improve(schedule):
    tmp = viewer(schedule)
    out = []
    result = []
    for day in tmp:
        nice = []
        start = STARTTIME
        if start < day[0]:
            start = day[0]
        end = day[0]
        for time in day:
            if is_time_after(end, time) == True:
                end = time

            else:
                endtime = time_24(str(increase(end, INTERVAL)))
                starttime = time_24(str(start))
                addon = starttime + " ~ " + endtime
                nice.append(addon)
                start = time
                end = time

        endtime = time_24(str(increase(end, INTERVAL)))
        starttime = time_24(str(start))
        addon = starttime + " ~ " + endtime
        nice.append(addon)
        result.append(nice)
    return result


def time_24(time):
    if time == "2400":
        return "0000"
    time = str(int(time))
    while len(time) < 4:
        time = "0" + time
    return time


def time_diff(t1, t2):
    count = 0
    t2 = int(t2)
    t1 = int(t1)
    while t1 < t2:
        count += 1
        t1 = int(increase(t1, INTERVAL))
    return count


def is_time_after(t1, t2):
    t1 = str(int(t1))
    t2 = str(int(t2))
    while len(t1) < 4:
        t1 = "0" + t1
    while len(t2) < 4:
        t2 = "0" + t2
    return increase(t1, INTERVAL) == (t2) or t1 == t2


def increase(time, duration):  # add duration to time
    time = int(time)
    if duration < 60:
        time += duration
        if time % 100 >= 60:
            time -= 60
            time += 100
        time = time_24(time)
        return time
    else:
        duration -= 60
        time += 100
        time = str(time)
        return increase(time, duration)

# mymods = get_freetime(url) # return modules taken by student
#matt_mods = get_freetime(url_matt)
