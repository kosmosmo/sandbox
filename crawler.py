import urllib.request
from bs4 import BeautifulSoup
import re,json

class Crawler():
    def __init__(self,id):
        self.url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(id,id)

    def get_soup(self, url, header):
        return BeautifulSoup(urllib.request.urlopen(url), 'html.parser')

    def crawl(self):
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(self.url, header)
        result = re.search('root.App.main = (.*)\;', soup.text)
        result = json.loads(result.group(1))
        pe = list(self.find('priceToBook',result))
        pb = list(self.find('trailingPE',result))
        if pe: pe = pe[0]['raw']
        if pb: pb = pb[0]['raw']
        return [pe,pb]

    def find(self,key,dictionary):
        if type(dictionary) != dict: return
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in self.find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.find(key, d):
                        yield result

a = Crawler("ERIC")
print (a.crawl())