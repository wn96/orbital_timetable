import platform
import sys
import os
from selenium import webdriver


def scrapper():

    # https://pymotw.com/3/platform/
    curr_os = platform.system()
    if (curr_os == "Windows"):
        subdir = "win"
    elif (curr_os == "Linux"):
        subdir = "linux"
    elif (curr_os == "Darwin"):
        subdir = "mac"
    else:
        print("Unknown OS")
        return None

    driver_path = os.path.join(
        os.getcwd(),
        "chromedriver",
        subdir,
        "chromedriver")
    sys.path.append(
        os.path.join(
            os.getcwd(),
            "chromedriver",
            subdir))  # redundancy

    options = webdriver.ChromeOptions()
    options.set_headless(True)
    try:
        browser = webdriver.Chrome(driver_path, chrome_options=options)
    except BaseException:
        browser = webdriver.Chrome(chrome_options=options)
    browser.get("http://nusmods.com/")
    week = browser.execute_script(
        'return document.getElementsByClassName("_1wFW83OO")[0].innerText')
    browser.quit()

    week = week.replace("\xa0", " ")
    sem, week_no = week.split(", Week ")
    return sem, int(week_no)


if __name__ == "__main__":
    print(scrapper())
