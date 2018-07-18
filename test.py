from lxml import etree
from io import open
import json
import csv,requests

api_url='http://localhost:3000/vulnerabilities/'
params={'id': '5b4d98dc7bd950121c2de2d6'}
r = requests.get(api_url,params=params)
print r.url

a=r.json()[0]
b=a['hostname'][0]['item'][0]['name']
print a['hostname'][0]['_id']
print b
