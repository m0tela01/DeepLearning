import os
import csv
import time
import requests

from csv import writer
from bs4 import BeautifulSoup
from selenium import webdriver

class Scraper:
    def __init__(self, stockTicker=input("Enter the Stock Ticker to scrape for: ")):
        self.rootSite = 'https://seekingalpha.com/symbol/' + str(stockTicker)
        self.dataStoreDir = "C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\project_data\\scrape_text\\seekingalpha\\" + str(stockTicker).lower() + "\\scraped_stories\\"
        self.response = requests.get(self.rootSite)
        self.scrollAmount = 500
        self.driver = webdriver.Chrome('C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\DeepLearning\\text-summarization\\chromedriver.exe')
        self.driver.get(self.rootSite)
        self.subDomain = 'https://seekingalpha.com/pr/'
        self.allLinks = []
        self.csvLinks = []
        self.indexId = 1
        self.wd = os.getcwd() + '\\text-summarization\\scrapes\\'
        self.title = ''
        time.sleep(3)   ####### pause and do capctcha -- !!put a break point here!!

    def c(self, element):
        element.click()

    def scrollDown(self):
        self.scrollAmount += 500
        self.driver.execute_script("window.scrollTo(0, "+ str(self.scrollAmount)+ ")")

    def openSwitch(self, link):
        self.driver.execute_script("window.open('"+link+"', 'new_window')")
        self.driver.switch_to_window(self.driver.window_handles[1])

    def closeSwitch(self):
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def getToPressReleases(self):
        rightSideFeed = self.driver.find_element_by_css_selector('.feed.news')
        dropdown = rightSideFeed.find_element_by_class_name('selector-title')
        self.c(dropdown)
        newsFeed = rightSideFeed.find_elements_by_class_name('feed-menu')[0]
        pressRelease = newsFeed.find_element_by_class_name('press-release')
        try:    ##if its already on press release then just pass -- should be an assert 
            self.c(pressRelease)
            time.sleep(3)
        except:
            pass

    def readLinksCsv(self):
        with open(self.wd + "alphaLinks.csv", 'r') as linksCSV:
                for row in linksCSV:
                    if row is not '\n':
                        self.allLinks.append(row.split(',')[1])
                    
                self.csvLinks = self.allLinks.copy()
                if len(self.csvLinks) is not 0:
                    self.indexId = len(self.csvLinks) + 1

    
    def writeNewLinksCsv(self, newLink):
        with open(self.wd + "alphaLinks.csv", 'a+', newline='') as linksCSV:
            writer = csv.writer(linksCSV, delimiter=',')
            if newLink not in self.csvLinks:
                writer.writerow([self.indexId, newLink, self.title]) #str(newLinks[i]).split(self.subDomain)[1]])
                self.indexId += 1

    def writePressRelease(self, paragraphs):
        with open(os.path.join(self.dataStoreDir, (self.title + ".txt")), 'w', encoding='utf-8') as story:
            for paragraph in paragraphs:
                story.write(str(paragraph.text) + '\n')

    def scrapeData(self):
        try:
            self.readLinksCsv()

            while True:            
                previousLinkCount = len(self.allLinks)
                currentLinkCount = len(self.allLinks)

                newLinks = []
                while previousLinkCount is currentLinkCount:
                    self.scrollDown()
                    ## need to reinitialize and test if everything is the same
                    rightSideFeed = self.driver.find_element_by_css_selector('.feed.news') ## this becomes stale
                    releases = rightSideFeed.find_element_by_class_name('press-releases')
                    releases = releases.find_elements_by_css_selector('.title.symbol_item [href]')

                    previousLinkCount = len(self.allLinks)
                    newLinks = []
                    for ele in releases:
                        link = ele.get_attribute('href')
                        if link not in self.csvLinks:
                            self.allLinks.append(link)
                            newLinks.append(link)
                        else:
                            continue
                    currentLinkCount = len(self.allLinks)
                

                for link in newLinks:
                    if link not in self.csvLinks:
                        self.openSwitch(link)
                        soup = BeautifulSoup(self.driver.page_source)

                        ## article text
                        overlay = soup.find(id='page_content_wrapper').find(class_='container').find(class_='row')
                        mainc = overlay.find(id='main_content').find(id='pr-body')
                        ps = mainc.select('p')
                        
                        self.title = str(link).split(self.subDomain)[1]
                        self.writeNewLinksCsv(link)
                        self.csvLinks.append(link)

                        self.writePressRelease(ps)
                        self.closeSwitch()
                        time.sleep(5)

                ## scroll down and get more links
                self.scrollDown()
        except Exception as ex:
            print('☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃')
            print(ex)
            self.scrapeData()   ####### pause and do capctcha -- !!put a break point here!!

def main():
    scrapper = Scraper()
    scrapper.getToPressReleases()   ####### pause and do capctcha -- !!put a break point here!!
    scrapper.scrapeData()


if __name__ == '__main__': main()