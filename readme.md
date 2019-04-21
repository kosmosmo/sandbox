# crawler

PE Ration, Price/Book crawler

## Prerequisites



```bash
Python 3.6
pip install bs4
```

## Usage

```python
from crawler import Crawler

companyList = ["AAPL","GOOG"]
Crawler.main(companyList) #return PERation and Price/Book in hashmap
Crawler.tojson(companyList) #merge new data to local cache data

###
{'AAPL': [16.818745, 8.178937], 'GOOG': [28.290277, 4.841371]}
###
```
