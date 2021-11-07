from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pyperclip


def recognition(audio_path):
    options = webdriver.ChromeOptions()

    options.add_argument('disable-gpu')
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(
        '/Users/muneung/Downloads/chromedriver', chrome_options=options)
    driver.get('https://nid.naver.com/nidlogin.login')
    driver.set_window_size(1920, 1080)
    time.sleep(3)

    uid = ''  # 네이버 id
    upw = ''  # 네이버 pw

    driver.find_element_by_name('id').click()
    pyperclip.copy(uid)
    driver.find_element_by_name('id').send_keys(Keys.COMMAND, 'v')

    driver.find_element_by_name('pw').click()
    pyperclip.copy(upw)
    driver.find_element_by_name('pw').send_keys(Keys.COMMAND, 'v')

    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    time.sleep(1)
    print('로그인성공')

    driver.get('https://clovanote.naver.com/home')
    time.sleep(1)

    driver.find_element_by_class_name('btn___2zdAC').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="container"]/div[1]/div[1]/div[1]/div[1]').click()
    time.sleep(1)
    print('임포트성공')
    driver.find_element_by_css_selector("input[type='file']").send_keys(
        audio_path)
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]').click()
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]').click()
    time.sleep(60)

    bs = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    news_tit = bs.findAll("span", {"class": "txt___1ymxJ"})

    speakers = []
    convers = []

    for a in range(len(news_tit)):
        if(a > 0):
            if("참석자" in news_tit[a-1].get_text()):
                speaker = news_tit[a-1].get_text()[4:]
                temp = news_tit[a].get_text()

                speakers.append(speaker)
                convers.append(temp)
            # else:
            #     temp = news_tit[a].get_text()[4:]

            #     convers.extend(temp)

    driver.close()

    return speakers, convers
