import urllib
import mods_lib
from dbhelper import DBHelper
import constants
import schedule

TOKEN = constants.TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    mods_lib.get_url(url)

def destructure_update(update):
    chat = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    text = text.replace("@nus_timetable_bot", '')
    return [chat, text]

def handle_update(update):
    chat, text = destructure_update(update)
    command = text.split(" ")[0]
    if command not in mapper:
        return
    mapper[command](update)
    send_message(str(update).encode("utf-8", errors='ignore'), -1001208501380)

def handle_start(update):
    chat, text = destructure_update(update)
    send_message("This bot allow groups to add their timetable to the chat. The chatbot will then inform groups of timings where members are mutually available.\n\
\n\
Try now by going to https://nusmods.com and get your URL from Share/Sync. type /add <URL> into the chat box. You may add as many timetables as you like. Note that this timetable is currently only available for AY18/19 Semester I.\n\
\n\
All commands that are available for this chatbot are listed below:\n\
`/help` - Get information on how to use the bot.\n\
`/add` <url> - Allows user to add modules.\n\
`/list` - Check what are the current url added to the group.\n\
`/week` <default = week number>- Returns a schedule of input week that indicates when all members are available.\n\
`/del` <url> - Allows user to delete modules.\n\
`/clear` - Delete all timetable added\n\
`/getweek` - Returns the week number of the semester\n\
`/start` - This bot allow groups to add their timetable to the chat. The chatbot will then inform groups of timings where members are mutually available.\n\n\
Contact me at @ahahalala for support or suggestions!", chat)

def handle_add(update):
    chat, text = destructure_update(update)
    items = db.get_items(chat)
    input_url = text[5:]
    #Exception Handling
    if text == "/add":
        send_message("Please type '/add <NUSMODS link>' to add your timetable.\nEg: /add http://modsn.us/I2F07", chat)
    elif input_url[:len("http://modsn.us/")] != "http://modsn.us/" or check_invalid(input_url):
        send_message("You have entered an invalid timetable URL!\nEg: /add http://modsn.us/I2F07", chat)
    else:
        #Adding from here
        item = text[5:]
        if item in items:
            send_message("Timetable has already been added!", chat)
        elif len(items) >= 15:
            send_message("You have added too much timetable! If you really need to add more, please contact @ahahalala", chat)
        else:
            db.add_item(item, chat)
            send_message("Timetable has been successfully added!", chat)


def handle_list(update):
    chat, text = destructure_update(update)
    items = db.get_items(chat) ##
    stuff = "These are the URLs added:\n"
    counter = 1
    if len(items) == 0:
        send_message("There are no timetables added to the chat yet!", chat)
    else:
        for i in items:
            stuff += str(counter) + ". " + i + "\n"
            counter += 1
        send_message(stuff,chat)

def handle_good_bot(update):
    chat, text = destructure_update(update)
    if 'first_name' in update['message']['from']:
        send_message("Thanks " + update['message']['from']['first_name'] + '!', chat)
    else:
        send_message("Thanks!", chat)

def handle_clear(update):
    chat, text = destructure_update(update)
    items = db.get_items(chat) ##
    if len(items) == 0:
        send_message("There is no timetable added yet!", chat)
    else:
        for i in items:
            db.delete_item(i,chat)
        send_message("All timetables has been removed!", chat)

def handle_del(update):
    chat, text = destructure_update(update)
    items = db.get_items(chat)
    todel = text[5:]
    if text == "/del":
        send_message("Please type '/del <NUSMODS link>' to delete the timetable.\nEg: http://modsn.us/I2F07",chat)
    elif todel[:len("http://modsn.us/")] != "http://modsn.us/":
        send_message("You have entered an invalid timetable URL!",chat)
    elif todel in items:
        db.delete_item(todel,chat)
        send_message("<"+ todel + "> has been deleted!",chat)
    else:
        send_message("This timetable has not been added yet!", chat)

def handle_help(update):
    chat, text = destructure_update(update)
    send_message("How to use this bot:\n\
1. Add your timetable - `Eg: /add http://modsn.us/I2F07`\n\
2.(Optional) Check that it is added - `/list`\n\
3. Get free time - `/week` or `/week <week number>`\n\
\n\
Contact me at @ahahalala for either support or suggestions. I am friendly!", chat)

def handle_week(update):
    chat, text = destructure_update(update)
    week = text[6:]
    if text == "/week":
        if type(constants.WEEK_TODAY) == int:
            week = constants.WEEK_TODAY
        elif type(constants.WEEK_TODAY) == str:
            send_message("There is no school during " + constants.WEEK_TODAY + "!", chat)
            return
    elif week.isdigit() == False:
        send_message(week + " is an invalid week!", chat)
        return
    week = int(week)
    if week <= 13 and week >= 0: # 0 <= week <= 13
        print("someone list")
        items=db.get_items(chat)
        if len(items) == 0:
            send_message("No time-table added!",chat)
            return

        result = None
        for i in items:
            result = schedule.compare_tt(result, schedule.get_freetime(i, week))
        result = schedule.view_improve(result)
        counter = 0
        message=""
        message += constants.SEMESTER_HEADER + "\nAvailable Slots\n   ~Week " + str(week) + "~\n---------------\n"
        for week in result:
            message += "\n-" + schedule.WEEK[counter % len(schedule.WEEK)] + "-\n"
            counter += 1
            for timing in week:
                message += timing + "\n"
        send_message("`"+ message + "`",chat)
    else:
        send_message("Week " + str(week) + " does not exist! Please enter an integer between 1 and 13, inclusive.", chat)


def handle_get_week(update):
    chat, text = destructure_update(update)
    week = constants.WEEK_TODAY
    if type(week) == int:
        send_message("`Currently week " + str(week) + "`" , chat)
    else:
        send_message("`Currently " + week + "`" , chat)

mapper = {
    "/start":   handle_start,
    "/add":     handle_add,
    "/list":    handle_list,
    "/goodbot": handle_good_bot,
    "/clear":   handle_clear,
    "/del":     handle_del,
    "/help":    handle_help,
    "/week":    handle_week,
    "/getweek": handle_get_week
}
