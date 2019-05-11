import urllib.request
from bs4 import BeautifulSoup
import re,json,collections
import csv
import os

class Crawler():
    def __init__(self):
        self.keys = ['priceToBook','trailingPE','fiftyTwoWeekLow']
        self.dic = collections.defaultdict(str)

    def main(self,ids):
        res = {}
        for id in ids:
            pe = pb = None
            c = self.crawl(id)
            if 'trailingPE' in c:
                pe = c['trailingPE']['raw']
            if 'priceToBook' in c:
                pb = c['priceToBook']['raw']
            res[id] = [pe,pb]
        return res

    def get_soup(self, url, header):
        return BeautifulSoup(urllib.request.urlopen(url), 'html.parser')


    def crawl(self,id):
        url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(id, id)
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url, header)
        result = re.search('root.App.main = (.*)\;', soup.text)
        result = json.loads(result.group(1))
        return self.find(result,self.keys)

    def find(self,dic, keys):
        res = collections.defaultdict()
        queue = []
        for key, val in dic.items():
            if key in keys:
                res[key] = val
            if type(val) == list or type(val) == dict:
                queue.append(val)
        while queue:
            q2 = []
            for item in queue:
                if type(item) == list:
                    for jtem in item:
                        if type(jtem) == list or type(jtem) == dict:
                            q2.append(jtem)
                elif type(item) == dict:
                    for key, val in item.items():
                        if key in keys:
                            res[key] = val
                        if type(val) == list or type(val) == dict:
                            q2.append(val)
            queue = q2
        return res

    def tojson(self,ids):
        res = self.main(ids)
        with open('data.json') as json_file:
            data = json.load(json_file)
        data = {**data, **res}
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        return res

    def toCSV(self,path):
        out = path[:-4] + '_out.csv'
        reader = csv.reader(open(path, "r"))
        with open(out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in reader:
                print (row)
                try:
                    if reader.line_num >= 1:
                        res = self.main([row[0]])[row[0]]
                        print (res)
                        if res[0]:
                            row.append(str(round(res[0], 2)))
                        else:row.append('')
                        if res[1]:
                            row.append(str(round(res[1], 2)))
                        else:
                            row.append('')
                        if res[0] and res[1]:
                            row.apppend(str(round(res[0]*res[1], 2)))
                        else:
                            row.append('')
                except:
                    pass
                writer.writerow(row)



Crawler().toCSV('oh.csv')

