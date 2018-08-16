# NUS Timetable Coordinator

[![CircleCI](https://circleci.com/gh/wn96/orbital_timetable/tree/master.svg?style=shield)](https://circleci.com/gh/wn96/orbital_timetable/tree/master)

**bot_username:** [nus_timetable_bot](https://t.me/nus_timetable_bot)

Run `pip install -r requirements.txt` prior to deployment.

## Description

This bot allow groups to add their timetable to the chat. The chatbot will then inform groups of timings where members are mutually available.

Try now by going to https://nusmods.com and get your URL from Share/Sync. In the telegram bot, type /add <URL> into the chat box. You may add as many timetables as you like, and type `/list` to see the timings where all time-tables are available

All commands that are available for this chatbot are listed below:

`/add` - Allows user to add modules.

`/list` - Check what are the current url added to the group.

`/week` - Returns a schedule of input week that indicates when all members are available.

`/del` - Allows user to delete modules.

`/clear` - Delete all timetable added

`/getweek` - Returns the week number of the semester

`/start` - Simple text to inform users of the bot functionalities.

Bot is currently hosted on a 1024 MB Server running on Ubuntu 18.04. There's funds to last 2.5 months, which will hopefully last until splashdown.

## Guide to using the bot
To use the bot, go to [nus_timetable_bot](https://t.me/nus_timetable_bot) and press start. Commands available will be populated. Add your timetable using /add <nusmods timetable>. To generate mutual free time, type /week (week_number). If no arguments is provided, timeslot for mutual free time for current week will be generated.

## Nice Pictures

![alt text](./images/screenshot1.png "Logo Title Text 1")

## Bugs/Issues and possible features for Milestone 3

- [x] `/check` command to allow users to see who added the timetable (Dictionary?)
- [x] Keep poking to check corner cases
- [x] Exception handling to ensure that program does not terminate on error.
- [x] Prevent adding of repeated timetables.
- [x] To remove telegram bot token from readme once orbital ended. We can't be bothered to gitignore it. :)
- [x] To return error message when wrong AY is provided.
- [x] Allow bot to work for all semesters.
- [x] Scrap current week from NUSMods for `/week`.
- [x] Query NUSMods API to get HTTP request for latest JSON file.

## Refactoring:
### These fixes are not done in orbital as they do not affect usability.

- [ ] Refactor bot_main.py to use OOP for commands. This should reduce clutters in the code, making the code base unreadable currently.


## Credits

Made by:

- [Ang Wei Neng](http://weineng.io)
- Peh Yu Xiang

Special thanks to:

- The NUS Orbital team for the opportunity to build our app for credits

- [Gareth Dwyer](https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay) for the tutorial on how to make a simple telegram bot.
