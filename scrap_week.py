import platform
<<<<<<< HEAD
import sys, os
from selenium import webdriver

=======
import sys
import os
from selenium import webdriver


>>>>>>> pr/2
def scrapper():

    # https://pymotw.com/3/platform/
    curr_os = platform.system()
<<<<<<< HEAD
    if (curr_os == "Windows"): subdir = "win"
    elif (curr_os == "Linux"): subdir = "linux"
    elif (curr_os == "Darwin"): subdir = "mac"
=======
    if (curr_os == "Windows"):
        subdir = "win"
    elif (curr_os == "Linux"):
        subdir = "linux"
    elif (curr_os == "Darwin"):
        subdir = "mac"
>>>>>>> pr/2
    else:
        print("Unknown OS")
        return None

<<<<<<< HEAD
    driver_path = os.path.join(os.getcwd(), "chromedriver", subdir, "chromedriver")
    sys.path.append(os.path.join(os.getcwd(), "chromedriver", subdir)) # redundancy
=======
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
>>>>>>> pr/2

    options = webdriver.ChromeOptions()
    options.set_headless(True)
    try:
        browser = webdriver.Chrome(driver_path, chrome_options=options)
<<<<<<< HEAD
    except:
        browser = webdriver.Chrome(chrome_options=options)
    browser.get("http://nusmods.com/")
    week = browser.execute_script('return document.getElementsByClassName("_1wFW83OO")[0].innerText')
=======
    except BaseException:
        browser = webdriver.Chrome(chrome_options=options)
    browser.get("http://nusmods.com/")
    week = browser.execute_script(
        'return document.getElementsByClassName("_1wFW83OO")[0].innerText')
>>>>>>> pr/2
    browser.quit()

    week = week.replace("\xa0", " ")
    sem, week_no = week.split(", Week ")
    return sem, int(week_no)

<<<<<<< HEAD
=======

>>>>>>> pr/2
if __name__ == "__main__":
    print(scrapper())
