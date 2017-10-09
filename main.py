from crawler import Crawler
from schemas import Page
from data_collector import DataCollector
import validators

dc = DataCollector('localhost', 27017, '20171009-morning')

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
        self.linkList = list()
        self.readLinks = []
        self.deep = 10
        self.cont = 0

    def setDeep(self, newDeep):
        self.deep = newDeep

    def addSeed(self, links):
        for link in links:
            self.linkList.append({'url': link, 'level': 0})

    def addLinks(self, links, parentLevel):
        for link in links:
            if Utils.isValidURL(link):
                self.linkList.append({'url': link, 'level': parentLevel+1})

    def startProcess(self):
        if len(self.linkList) == 0:
            print 'Insert seed urls'
        else:
            while len(self.linkList) > 0:
                if self.linkList[-1]['url'] not in self.readLinks and self.linkList[-1]['level'] <= self.deep:
                    self.cont = self.cont + 1
                    print 'Page ' + str(self.cont) +'====================================================='
                    print 'Working on: ' + self.linkList[-1]['url'] + ' --- level ' + str(self.linkList[-1]['level'])
                    webInfo = Crawler.getInfoFromOneWeb(self.linkList[-1]['url'])
                    self.readLinks.append(self.linkList[-1]['url'])
                    p = Page(self.linkList[-1]['url'], '', self.linkList[-1]['level'], self.linkList[-1]['url'], webInfo['links'], [], [])
                    dc.addData('collectionoftest', p.returnLikeObject())
                    self.addLinks(webInfo['links'], self.linkList[-1]['level'])

                self.linkList.pop()

            print '***** THE PROCESS HAS FINISHED *****'
            print 'READ PAGES: ' + str(len(self.readLinks))

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