# encoding:utf-8
import logging
import sys
import time


import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import db

# 配置
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('log-level=4')


# 随机一个合适的温度 range:[36.4,36.9)


def temperature():
    return 36.5

# 检测页面是否加载完成


def onPageLoad(driver):
    status = driver.find_element_by_css_selector('app-index')
    return status


def autoReport(userinfo: tuple):
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path='chromedriver')
    driver.get("https://stuhealth.jnu.edu.cn/#/login")
    # 填入账号密码
    driver.find_element_by_id("zh").send_keys(userinfo[0])
    driver.find_element_by_id("passw").send_keys(userinfo[1])
    # 提交
    driver.find_element_by_css_selector('[type=submit]').click()
    # 直到页面加载完成
    try:
        WebDriverWait(
            driver, timeout=5, poll_frequency=0.2).until(onPageLoad)
        # 开始提交 
        driver.find_element_by_id('10000').click()
        driver.find_element_by_id('tj').click()
        time.sleep(5)
    except Exception as e:
        logging.info(str(userinfo) +":已提交，无需重复提交")
        return False
    finally:
        driver.close()


# def shutdown_driver():
#     driver.close()
#     driver.quit()


def reprot_all():
    userlist = db.alluser()
    for user in userlist:
        print(user)
        # if user[0] != '202034241005':
        #     print("pass")
        #     continue
        try:
            print(autoReport(user))
        finally:
            pass
        time.sleep(30)




def start(work_time: str = '09:10:00'):
    schedule.every().day.at(work_time).do(reprot_all)
    # global stop
    stop = False
    while True:
        try:
            schedule.run_pending()
            # print(stop)
            time.sleep(1)
        finally:
            pass
    print('eixt')


if __name__ == '__main__':
    work_time = sys.argv[1] if len(sys.argv) > 1 else '09:10:00'
    print('auto report will work at', work_time)
    start(work_time)
