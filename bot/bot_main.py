import json
import time
import urllib
import mods_lib
from dbhelper import DBHelper
from command_map import handle_update
import constants

db = DBHelper()
TOKEN = constants.TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_updates(offset=None):
    try:
        url = URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = mods_lib.get_json_from_url(url)
        return js
    except Exception as e:
        print("ERROR HAS OCCURED IN GET_UPDATES", e)

def is_valid_update(update):
    return ("message" in update and
           "chat" in update["message"] and
           "text" in update["message"])

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    mods_lib.get_url(url)

def check_invalid(url):
    return mods_lib.expand_url(url) == "http://modsn.us" or mods_lib.expand_url(url) == "http://modsn.us/"

def handle_updates(updates):
    try:
        for update in updates["result"]:
            if is_valid_update(update):
                handle_update(update)

    except Exception as e:
        chat = update["message"]["chat"]["id"]
        send_message("An error has occured! Please try again. If the problem persist, please email support at weineng.a@gmail.com!", chat)
        print("ERROR has occured: ", e)
        send_message("ERROR HAS OCCURED", -1001208501380)
        print(str(update).encode("utf-8", errors='ignore'))
        print()


def main():
    db.setup()
    last_update_id = None
    print("Starting NUSMODS Timetable Coordinator")
    while True:
        updates = get_updates(last_update_id)
        if "result" in updates:
            if len(updates["result"]) > 0:
                last_update_id = mods_lib.get_last_update_id(updates) + 1
                print(updates)
                handle_updates(updates)
        time.sleep(0.5)

def build_keyboard(items):
    keyboard = [["/del " + item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

if __name__ == '__main__':
    main()
