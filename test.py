from lxml import etree
from io import open
import json
import csv,requests as req
import pandas as pd
import numpy as np

# api_url='http://localhost:3000/vulnerabilities/vuln'
# params={'id': '5b504155787dd30fe86d4255'}
# r = requests.get(api_url,params=params)
# print r.url
# print r.text

# a=r.json()
# b=a['hostname'][0]['item'][0]['name']
# print a['hostname'][0]['_id']
# print b
idFile='5b5fcb41cb827b21680fcb19'
find_data='http://localhost:3000/compliance/comp'
parameterDownload={'id':idFile}
dataFile=req.get(find_data,params=parameterDownload)
dataDownload = dataFile.json()
# print dataDownload['item']
items = dataDownload['item']
df = pd.DataFrame(np.array(items))
df.to_csv('test.csv',sep='\t')