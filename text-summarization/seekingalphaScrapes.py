import csv
import json
import re
import time

from csv import writer
from datetime import datetime
from pprint import pprint

# import pyrebase

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Sets up Date and time locally
# javaScriptDays = {days: [] for days in range(7)}
# status = ''
# currentTime = datetime.utcnow().time().replace(second=0,microsecond=0)
# currentWeekDay = datetime.today().weekday()
# currentWeekDay = currentWeekDay + 1
# if currentWeekDay == 7:
#    currentWeekDay = 0


# parse the main website

rootSite = 'https://seekingalpha.com/pr/17803996-nvidia-gtc-news-to-be-shared-on-march-24-followed-investor-call'

rootSite = 'https://seekingalpha.com/symbol/NVDA'
rootSite = 'https://seekingalpha.com/symbol/NVDA?news=press-release' ##doesnt work

seekingAlpha = 'https://seekingalpha.com/symbol'
response = requests.get(rootSite)
soup = BeautifulSoup(response.text, 'html.parser')



def c(element):
    element.click()

def scrollDown(scrollAmount):
    scrollAmount += 500
    driver.execute_script("window.scrollTo(0, "+ str(scrollAmount)+ ")")
    return scrollAmount

def openSwitch(link):
    driver.execute_script("window.open('"+link+"', 'new_window')")
    driver.switch_to_window(driver.window_handles[1])

def closeSwitch():
    driver.close()
    driver.switch_to_window(driver.window_handles[0])


##root site
# feed = soup.find(id='page_content_wrapper').find(class_='row').find(id='main_content').find(class_='bottom-content')

driver = webdriver.Chrome('C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\project\\chromedriver.exe')
driver.get(rootSite)

####### pause and do capctcha
time.sleep(5)

rightSideFeed = driver.find_element_by_css_selector('.feed.news')
dropdown = rightSideFeed.find_element_by_class_name('selector-title')
c(dropdown)
newsFeed = rightSideFeed.find_elements_by_class_name('feed-menu')[0]
pressRelease = newsFeed.find_element_by_class_name('press-release')
try:
    c(pressRelease)
except:
    pass

# newsFeed.find_element_by_l



    
allLinks = []
scrollAmount = 500
while True:

    
    rightSideFeed = driver.find_element_by_css_selector('.feed.news') ## this becomes stale
    releases = rightSideFeed.find_element_by_class_name('press-releases')
    releases = releases.find_elements_by_css_selector('.title.symbol_item [href]')
    
    previousLinkCount = len(allLinks)
    currentLinkCount = len(allLinks)

    newLinks = []
    while previousLinkCount is currentLinkCount:
        previousLinkCount = len(allLinks)
        scrollAmount = scrollDown(scrollAmount)
        newLinks = []
        for ele in releases:
            link = ele.get_attribute('href')
            if link not in allLinks:
                allLinks.append(link)
                newLinks.append(link)
        currentLinkCount = len(allLinks)
    # links = [elem.get_attribute('href') for elem in releases]

    # storesAccessible = len(releases)
    for link in newLinks:
        openSwitch(link)
        soup = BeautifulSoup(driver.page_source)

        ## article text
        overlay = soup.find(id='page_content_wrapper').find(class_='container').find(class_='row')
        mainc = overlay.find(id='main_content').find(id='pr-body')
        ps = mainc.select('p')

        for paragraph in ps:
            print(paragraph)

        ## article text

        closeSwitch()
        time.sleep(5)

    ## scroll down and get more
    scrollDown(scrollAmount)


