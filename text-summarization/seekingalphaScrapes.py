import csv
import time
import requests

from csv import writer
from bs4 import BeautifulSoup
from selenium import webdriver

class Scraper:
    def __init__(self, stockTicker=input("Enter the Stock Ticker to scrape for: ")):
        self.rootSite = 'https://seekingalpha.com/symbol/' + str(stockTicker)
        self.dataStoreDir = "C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\project_data\\scraped_stories"
        self.seekingAlpha = 'https://seekingalpha.com/symbol'
        self.response = requests.get(self.rootSite)
        self.scrollAmount = 500
        self.driver = webdriver.Chrome('C:\\Users\\Telahun\\Documents\\School\\CECS590 - Deep Learning\\DeepLearning\\text-summarization\\chromedriver.exe')
        self.driver.get(self.rootSite)
        self.subDomain = 'https://seekingalpha.com/pr'
        self.allLinks = []
        self.indexId = 1
        self.title = ''
        time.sleep(5)   ####### pause and do capctcha -- !!put a break point here!!

    def c(self, element):
        element.click()

    def scrollDown(self):
        self.scrollAmount += 500
        driver.execute_script("window.scrollTo(0, "+ str(scrollAmount)+ ")")

    def openSwitch(self, link):
        driver.execute_script("window.open('"+link+"', 'new_window')")
        driver.switch_to_window(driver.window_handles[1])

    def closeSwitch(self):
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

    def getToPressReleases(self):
        rightSideFeed = self.driver.find_element_by_css_selector('.feed.news')
        dropdown = rightSideFeed.find_element_by_class_name('selector-title')
        self.c(dropdown)
        newsFeed = rightSideFeed.find_elements_by_class_name('feed-menu')[0]
        pressRelease = newsFeed.find_element_by_class_name('press-release')
        try:    ##if its already on press release then just pass -- should be an assert 
            self.c(pressRelease)
        except:
            pass

    def readLinksCsv(self):
        with open("links.csv", 'a+') as linksCSV:
                for row in linksCSV:
                    self.allLinks.append(row.split()[1])
    
    def writeNewLinksCsv(self, newLinks):
        with open("links.csv", 'a+') as linksCSV:
            writer = csv.writer(linksCSV, delimiter=',')
            for i in range(0, len(newLinks)):
                writer.writerow([self.indexId, newLinks[i], self.title]) #str(newLinks[i]).split(self.subDomain)[1]])
                self.indexId += 1

    def writePressRelease(self, paragraphs):
        with open(self.title + ".txt", 'w') as story:
            for paragraph in paragraphs:
                story.write(paragraph)

    def scrapeData(self):
        self.readLinksCsv()
        while True:
            ## need to reinitialize and test if everything is the same
            rightSideFeed = self.driver.find_element_by_css_selector('.feed.news') ## this becomes stale
            releases = rightSideFeed.find_element_by_class_name('press-releases')
            releases = releases.find_elements_by_css_selector('.title.symbol_item [href]')
            
            previousLinkCount = len(self.allLinks)
            currentLinkCount = len(self.allLinks)

            newLinks = []
            while previousLinkCount is currentLinkCount:
                previousLinkCount = len(self.allLinks)
                self.scrollDown(scrollAmount)
                newLinks = []
                for ele in releases:
                    link = ele.get_attribute('href')
                    if link not in allLinks:
                        self.allLinks.append(link)
                        newLinks.append(link)
                currentLinkCount = len(allLinks)
            
            # self.writeNewLinksCsv(newLinks)

            # links = [elem.get_attribute('href') for elem in releases]

            # storesAccessible = len(releases)
            for link in newLinks:
                self.openSwitch(link)
                soup = BeautifulSoup(driver.page_source)

                ## article text
                overlay = soup.find(id='page_content_wrapper').find(class_='container').find(class_='row')
                mainc = overlay.find(id='main_content').find(id='pr-body')
                ps = mainc.select('p')
                
                self.title = str(link).split(self.subDomain)[1]
                self.writeNewLinksCsv([link])

                self.writePressRelease(ps)
                self.closeSwitch()
                time.sleep(5)

            ## scroll down and get more links
            self.scrollDown()

# def getTicker():
#     ticker = ''
#     while ticker is '':
#         ticker = input("Enter the Stock Ticker to scrape for: ")
#     return ticker


def main():
    scrapper = Scraper()
    scrapper.getToPressReleases()   ####### pause and do capctcha -- !!put a break point here!!
    scrapper.scrapeData()


if __name__ == '__main__': main()