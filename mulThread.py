import urllib.request
from bs4 import BeautifulSoup
import re,json,collections
import csv
import os
from threading import Thread

symList = []
ans = collections.defaultdict(list)

def crawl(sym):
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(sym, sym)
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(url), 'html.parser',from_encoding="iso-8859-1")
    result = re.search('root.App.main = (.*)\;', soup.text)
    result = json.loads(result.group(1))
    dic = result
    keys = ['priceToBook','trailingPE']
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
    nums = ['','','']
    if 'trailingPE' in res and 'raw' in res['trailingPE']:
        pe = res['trailingPE']['raw']
        nums[0] = pe
    if 'priceToBook' in res and 'raw' in res['priceToBook']:
        pb = res['priceToBook']['raw']
        nums[1] = pb
    if nums[0] != '' and nums[1] != '':
        exb = str(round(nums[0]*nums[1],2))
        nums[2] = exb
    ans[sym] = nums
    print (sym,nums)


def toSyms(path):
    reader = csv.reader(open(path, "r"))
    for row in reader:
        symList.append(row[0].replace(' ',''))
    return symList



path = 'st.csv'
toSyms(path)

threads = []
for key in symList[0:200]:
    t = Thread(target=crawl, args=(key,))
    t.start()
    threads.append(t)
for b in threads:
    b.join()
print (len(ans))
print (ans)


