import os
import csv
import time
import requests

from csv import writer
from bs4 import BeautifulSoup
from selenium import webdriver

##use dictionaries

class Scraper:
    def __init__(self, stockTicker=input("Enter the Stock Ticker to scrape for: ")):
        self.rootSite = 'https://www.barchart.com/stocks/quotes/' + str(stockTicker) + '/news'
        self.dataStoreDir = "C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\project_data\\scrape_text\\barchart\\" + str(stockTicker).lower() + "\\scraped_stories\\"
        self.response = requests.get(self.rootSite)
        self.scrollAmount = 600
        self.scrollCount = 0
        self.driver = webdriver.Chrome('C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\DeepLearning\\text-summarization\\chromedriver.exe')
        self.driver.get(self.rootSite)
        self.subDomain = ('https://www.barchart.com/story/stocks/quotes/' + str(stockTicker) + '/news/').lower()
        self.allLinks = []
        self.csvLinks = {}
        self.indexId = 1
        self.wd = os.getcwd() + '\\scrapes\\'
        self.title = ''
        time.sleep(3)   ####### pause and do capctcha -- !!put a break point here!!

    def c(self, element):
        element.click()

    def scrollDown(self):
        self.scrollAmount += 500
        self.scrollCount += 1
        self.driver.execute_script("window.scrollTo(0, "+ str(self.scrollAmount)+ ")")
        if self.scrollCount % 3 is 0:
            loadMore = self.driver.find_element_by_class_name('bc-load-more-stories-block')
            self.c(loadMore)
            time.sleep(2)

    def openSwitch(self, link):
        self.driver.execute_script("window.open('"+link+"', 'new_window')")
        self.driver.switch_to_window(self.driver.window_handles[1])

    def closeSwitch(self):
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def getToPressReleases(self):
        stories = self.driver.find_element_by_class_name('stories-list')
        return stories.find_elements_by_css_selector('.story.clearfix')


    def readLinksCsv(self):
        with open(self.wd + "barchartLinks.csv", 'r') as linksCSV:
                for row in linksCSV:
                    if row is not '\n':
                        # self.allLinks.append(row.split(',')[1])
                        self.csvLinks[row.split(',')[1]] = row.split(',')[0]
                    
                # self.csvLinks = self.allLinks.copy()
                if len(self.csvLinks) is not 0:
                    self.indexId = len(self.csvLinks) + 1

    
    def writeNewLinksCsv(self, newLink):
        with open(self.wd + "barchartLinks.csv", 'a+', newline='') as linksCSV:
            writer = csv.writer(linksCSV, delimiter=',')
            if newLink not in self.csvLinks:
                writer.writerow([self.indexId, newLink, self.title]) #str(newLinks[i]).split(self.subDomain)[1]])
                self.indexId += 1

    def writePressRelease(self, paragraphs):
        if len(self.title) >= 240:
            self.title = self.title[:220]
        with open(os.path.join(self.dataStoreDir, (self.title + ".txt")), 'w', encoding='utf-8') as story:
            for paragraph in paragraphs:
                story.write(str(paragraph.text) + '\n')

    def scrapeData(self):
        try:
            self.readLinksCsv()

            while True:            
                # previousLinkCount = len(self.allLinks)
                # currentLinkCount = len(self.allLinks)

                newLinks = []
                while len(newLinks) == 0:
                    self.scrollDown()
                    time.sleep(1)
                    ## need to reinitialize and test if everything is the same
                    releases = self.getToPressReleases() ## this becomes stale

                    previousLinkCount = len(self.allLinks)
                    newLinks = []
                    for ele in releases:
                        link = ele.find_element_by_class_name('story-link').get_attribute('href')
                        if link not in self.csvLinks:
                            # self.allLinks.append(link)
                            newLinks.append(link)
                        else:
                            continue
                    # currentLinkCount = len(self.allLinks)
                

                for link in newLinks:
                    if 'barchart' in link:
                        self.openSwitch(link)
                        time.sleep(2)
                        soup = BeautifulSoup(self.driver.page_source)
                        self.title = str(link).split(self.subDomain)[1].split('/')[1]

                        ## article text
                        overlay = soup.find(class_='column-inner').find(class_='modal-inner').find(class_='article-content')
                        ps = overlay.select('p')

                        self.writePressRelease(ps)                        
                        self.writeNewLinksCsv(link)
                        self.csvLinks[link] = self.indexId

                        self.closeSwitch()
                        time.sleep(2)

                ## scroll down and get more links
                self.scrollDown()
        except Exception as ex:
            print('☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃☃')
            print(ex)
            self.driver.switch_to_window(self.driver.window_handles[0])
            self.scrapeData()   ####### pause and do capctcha -- !!put a break point here!!

def main():
    scrapper = Scraper()
    _ = scrapper.getToPressReleases()   ####### pause and do capctcha -- !!put a break point here!!
    scrapper.scrapeData()


if __name__ == '__main__': main()
