from lxml import etree
from io import open
import json
import csv,requests

api_url='http://localhost:3000/vulnerabilities/'
params={'id': '5b4ff94f70aeba0e443885cf'}
r = requests.get(api_url,params=params)
print r.url
print r.text

# a=r.json()[0]
# b=a['hostname'][0]['item'][0]['name']
# print a['hostname'][0]['_id']
# print b
