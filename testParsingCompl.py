from lxml import etree
from collections import defaultdict
import csv,json
i=0
report = {}
reportHostName = []
reportItem = []
f = open('D:/project/file xl/10_23_67_85_ffes3i.nessus', 'r')
xml_content = f.read()
f.close()
root = etree.fromstring(xml_content)
for block in root:
    if block.tag == "Report":
        for report_host in block:
            if report_host.tag=="ReportHost":
                System = report_host.attrib['name']
                
                reportItem = []
                for report_item in report_host:
                    if report_item.tag=="ReportItem":
                        i=i+1
                        iStatus=report_item.attrib['severity']
                        for param in report_item:
                            if param.tag=="{http://www.nessus.org/cm}compliance-check-name":
                                title=param.text
                            elif param.tag=="{http://www.nessus.org/cm}compliance-result":
                                status=param.text
                            elif param.tag =="description":
                                result=param.text
                                detail=param.text
                        reportItem.append({
                            'system': System,
                            'title': title,
                            'status': status,
                            'result': result,
                            'detail': detail,
                            'iStatus':iStatus,
                        })
            reportHostName.append(
                reportItem
            )
    
print json.dumps(reportHostName)




with open('report HostName.txt', 'w') as f:
    f.write(unicode(reportHostName))
f = csv.writer(open("compl.csv", "wb+"))

f.writerow(["System", "Title", "Status","result", "iStatus","Detail"])

for x in range (0,len(reportHostName)):
    for y in range (0,len(reportHostName[x])):
        f.writerow([reportHostName[x][y]["system"],
                    reportHostName[x][y]["title"],
                    reportHostName[x][y]["status"],
                    reportHostName[x][y]["result"],
                    reportHostName[x][y]["iStatus"],
                    reportHostName[x][y]["detail"],
                    ])
