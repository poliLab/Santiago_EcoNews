from crawler import Crawler
from schemas import Page
from data_collector import DataCollector
import validators

dc = DataCollector('localhost', 27017, '20171013-nigth')
readLinks = []

class Utils:

    invalidWords = ['facebook', 'fb', 'google', 'instagram', 'twitter', 'youtube', 'bing', 'yahoo',
    'ecosia', '.pdf', '.doc', '.xls', '.png', '.jpg', '.gif', 'ads', 'goo.gl', 'microsoft',
    'gmail', 'skype', 'download', 'apple', 'pinterest', '.ppt', 'mozilla', 'microsoft', 'ebay', 'amazon',
    'newegg', 'soundcloud', 'advertise', 'advertising']

    @staticmethod
    def isValidURL(url):
        containsInvalidWord = False

        try:
            url = str(url)
            for word in Utils.invalidWords:
                if url.find(word) > -1:
                    containsInvalidWord = True
                    break

            if validators.url(url) and containsInvalidWord == False:
                return True
            else:
                return False

        except:            
            return False

class MainCrawler:
    
    def __init__(self):
        self.seed = []
        self.deep = 10

    def setDeep(self, newDeep):
        self.deep = newDeep

    def addSeed(self, links):
        for link in links:
            self.seed.append(link)

    @staticmethod
    def extractLinks(url, depth, maxDepth):
        if Utils.isValidURL(url) and url not in readLinks:
            readLinks.append(url)
            webInfo = Crawler.getInfoFromOneWeb(url)
            print('===== Working on: ' + url + ' --- depth: ' + str(depth) + ' --- ' +str(len(webInfo['links'])) + ' links were found')
            p = Page(url, '', depth, url, webInfo['links'], [], [])
            dc.addData('collectionoftest', p.returnLikeObject())
            depth = depth + 1
            if depth < maxDepth :
                for newUrl in webInfo['links']:
                    MainCrawler.extractLinks(newUrl, depth, maxDepth)
            else:
                return
        

    def startProcess(self):
        if len(self.seed) == 0:
            print('Insert seed urls')
        else:
            for link in self.seed:
                MainCrawler.extractLinks(link, 0, self.deep)

        print('***** THE PROCESS HAS FINISHED *****')
        print(str(len(readLinks)) + ' read links')

mc = MainCrawler()
seed = [
    'http://www.eluniverso.com/servicios/rss',
    'http://www.ecoticias.com/',
    'http://www.ecologiahoy.com',
    'http://www.eltiempo.com/noticias/ecologia',
    'https://www.elheraldo.co/ecologia',
    'http://www.elcolombiano.com/medio-ambiente',
    'http://www.elespectador.com/noticias/medio-ambiente',
    'http://www.wwf.org.co/medioambiente.cfm'
]

mc.addSeed(seed)
mc.setDeep(5)
mc.startProcess()