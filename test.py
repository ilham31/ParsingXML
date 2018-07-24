from lxml import etree
from io import open
import json
import csv,requests

# api_url='http://localhost:3000/vulnerabilities/vuln'
# params={'id': '5b504155787dd30fe86d4255'}
# r = requests.get(api_url,params=params)
# print r.url
# print r.text

# a=r.json()
# b=a['hostname'][0]['item'][0]['name']
# print a['hostname'][0]['_id']
# print b

get_url='https://simak.ipb.ac.id/Account/Login'
readData = requests.post(get_url)
fileVuln=readData.json()
print len(fileVuln)
print fileVuln
if (len(fileVuln)<1):
    return "file kosong"
else:
    file1=fileVuln[0]
    return file1

Jsondata=json.dumps(data)
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
r=requests.get(api_url,data=Jsondata,headers=headers)
print r.text()
# print r.json()
# print r.text()