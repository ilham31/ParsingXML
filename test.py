from lxml import etree
from io import open
import json
import csv,requests

api_url='http://localhost:3000/vulnerabilities/vuln'
params={'id': '5b504155787dd30fe86d4255'}
r = requests.get(api_url,params=params)
print r.url
print r.text

a=r.json()
b=a['hostname'][0]['item'][0]['name']
print a['hostname'][0]['_id']
print b
