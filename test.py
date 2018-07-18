from lxml import etree
from io import open
import json
import csv,requests

api_url='http://localhost:3000/vulnerabilities/'
r = requests.get(api_url,params='5b4d881ab6543f410411ac11')
print r.url
# from collections import defaultdict
# i=0
# report = {}
# reportHostName = []
# reportItem = []
# f = open('D:/project/file xl/10_23_67_85-mbss_6htdj9.nessus', 'r')
# xml_content = f.read()
# f.close()
# root = etree.fromstring(xml_content)
# for block in root:
#     if block.tag == "Report":
        
#         for report_host in block:
#             if report_host.tag=="ReportHost":
#                 Hostname = report_host.attrib['name']
#                 reportItem = []
#                 for report_item in report_host:
#                     if report_item.tag=="ReportItem":
                        
#                         portProtocol = report_item.attrib['svc_name'] +"/" +report_item.attrib['protocol']
#                         severity = report_item.attrib['severity']
#                         name = report_item.attrib['pluginName'] +" ("+report_item.attrib['pluginID']+")"
#                         for param in report_item:
#                             if param.tag=="solution":
#                                 solution = param.text

#                             elif param.tag=="synopsis":
#                                 synopsis=param.text

#                             elif param.tag =="risk_factor":
#                                 risk_factor=param.text

#                             elif param.tag =="description":
#                                 desc=param.text

#                         detail = synopsis + desc

#                         reportItem.append({
#                             "hostname": Hostname,
#                             "name": name,
#                             "severity": severity,
#                             "port/protocol": portProtocol,
#                             "solution": solution,
#                             "synopsis": synopsis,
#                             "detail": detail,
#                             "risk_level": risk_factor
#                         })
#                 reportHostName.append(
#                     reportItem
#                 )

#     # report = {
#     #     reportHostName
#     # }
# # print reportHostName[0]
# # print reportHostName[0][1]
# # print reportHostName

# # with open("datavuln.csv", "w") as output:
# #     writer = csv.writer(output, lineterminator='\n')
# #     writer.writerows(reportHostName)
# # print len(reportHostName)
# with open('report HostName.txt', 'w') as f:
#     f.write(unicode(reportHostName))
# f = csv.writer(open("vulnv.csv", "wb+"))

# # # Write CSV Header, If you dont need that, remove this line
# f.writerow(["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity"])

# for x in range (0,len(reportHostName)):
#     for y in range (0,len(reportHostName[x])):
#         # print reportHostName[x][y]["hostname"]
#         f.writerow([reportHostName[x][y]["hostname"],
#                     reportHostName[x][y]["name"],
#                     reportHostName[x][y]["port/protocol"],
#                     reportHostName[x][y]["risk_level"],
#                     reportHostName[x][y]["synopsis"],
#                     reportHostName[x][y]["detail"],
#                     reportHostName[x][y]["solution"],
#                     reportHostName[x][y]["severity"],
#                     ])
# # with open('datavuln.csv', 'wb') as myFile:
# #     w = csv.writer(myFile, dialect='excel')
# #     w.writerows(reportHostName)
# # myFile.close()

# # parsed = json.loads(reportHostName).read()
# # print json.dumps(parsed)
# # hasil = open('hasilTes.py', 'wb')
# # hasil.write(unicode(reportHostName[0]))
# # # hasil.truncate()
# # # hasil.close()

# # hasil2 = open('hasilTes2.py', 'wb')
# # hasil2.write(unicode(reportHostName[1]))
# # hasil2.truncate()
# # hasil2.close()
# # print reportHostName