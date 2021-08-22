import os
import shutil
import stat
from pathlib import Path

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

global driver

def add_execute_permission(path: Path, target: str = "u"):
    """Add `x` (`execute`) permission to specified targets."""
    mode_map = {
        "u": stat.S_IXUSR,
        "g": stat.S_IXGRP,
        "o": stat.S_IXOTH,
        "a": stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    }

    mode = path.stat().st_mode
    for t in target:
        mode |= mode_map[t]

    path.chmod(mode)

def settingDriver():
    print("driver setting")
    global driver

    driverPath = "/tmp" + "/chromedriver"
    headlessPath = "/tmp" + "/headless-chromium"
    PROXY = os.environ.get('PROXY')

    # copy and change permission
    print("copy headless-chromium")
    shutil.copyfile(os.getcwd() + "/headless-chromium", headlessPath)
    add_execute_permission(Path(headlessPath), "ug")

    print("copy chromedriver")
    shutil.copyfile(os.getcwd() + "/chromedriver", driverPath)
    add_execute_permission(Path(driverPath), "ug")

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = headlessPath

    # PORT = int(os.environ.get("PORT", 8080))
    print("get driver")
    driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)

def seleniumSample(request):
    settingDriver()
    global driver

    driver.get('https://www.covid19-vaccine.mrso.jp/osaka/VisitNumbers/visitnoAuth/')
    time.sleep(10)
    driver.find_element_by_id('VisitnoAuthName').send_keys('271004')
    driver.find_element_by_id('VisitnoAuthVisitno').send_keys(os.environ.get('ID'))
    Select(driver.find_element_by_id('VisitnoAuthYear')).select_by_value(os.environ.get('YEAR'))
    Select(driver.find_element_by_id('VisitnoAuthMonthMonth')).select_by_value(os.environ.get('MONTH'))
    Select(driver.find_element_by_id('VisitnoAuthDayDay')).select_by_value(os.environ.get('DAY'))
    driver.find_element_by_class_name('auth-btn').click()
    time.sleep(5)
    driver.find_element_by_class_name('btn-next').click()
    time.sleep(5)
    subject = driver.find_element_by_css_selector('.plan-subject a').text
    print(subject)
    driver.find_element_by_class_name('covid19_move_plan_detail').click()
    time.sleep(5)
    for target in driver.find_elements_by_css_selector('#calendar-table > tbody > tr > td > a'):
        if (target.text == '×'):
            print('残念！')
        else:
            print('やった！')
            return 'Reserve success.'
    driver.quit()
    return 'Reserve failed.'