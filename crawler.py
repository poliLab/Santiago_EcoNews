import requests
from bs4 import BeautifulSoup

class Crawler:

    @staticmethod
    def getLinksFromOneWeb(web):
        request = requests.get(web)
        soup = BeautifulSoup(request.text, 'html.parser')
        aList = []

        for link in soup.find_all('a'):
            aList.append(link.get('href'))

        return aList

    @staticmethod
    def getInfoFromOneWeb(web):

        print('Getting info from ' + web)

        try:
            request = requests.get(web, timeout=5)
            soup = BeautifulSoup(request.text, 'html.parser')

            title = web

            description = soup.findAll(attrs={"name":"description"})
            aList = []
            headlineList = []

            for link in soup.find_all('a'):
                aList.append(link.get('href'))

            for headline in soup.find_all('h1'):
                headlineList.append(headline.text)

            for headline in soup.find_all('h2'):
                headlineList.append(headline.text)

            return {
                    'title': title,
                    'links': aList,
                    'headlines': headlineList
            }

        except:

            print('HTTP ERROR')

            return {
                    'title': web,
                    'links': [],
                    'headlines': []
            }

    @staticmethod
    def getLinksFromArray(links = []):

        collectedLinks = []
        
        for link in links:
            request = requests.get(link.strip('\r\n').strip('\r').strip('\n'))
            soup = BeautifulSoup(request.text, 'html.parser')

            for element in soup.find_all('a'):
                collectedLinks.append(element.get('href'))

        return collectedLinks

#Crawler.getLinksFromOneWeb('http://www.mundoenlaces.com', 'result.dat')
#Crawler.getLinksFromSeveralsWeb('source.dat', 'several-result.dat')
#Crawler.getLinksFromArray(['http://bing.com', 'http://yahoo.com', 'http://ecosia.org'])
