from lxml import etree
import os
from collections import defaultdict
import csv,json,requests as req

def compl(filename):
        os.chdir('D:/ilham/ParsingXML/data')
        api_url='http://localhost:3000/compliance'
        i=0
        report = {}
        reportHostName = []
        reportItem = []
        # data =[]
        f = open(filename, 'r')
        xml_content = f.read()
        f.close()
        root = etree.fromstring(xml_content)
        for block in root:
            if block.tag == "Report":
                for report_host in block:
                    if report_host.tag=="ReportHost":
                        System = report_host.attrib['name']
                        # reportItem = []
                        for report_item in report_host:
                            if report_item.tag=="ReportItem":
                                # i=i+1
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
                                    'i_status':iStatus,
                                })
                        # reportHostName.append({
                        #     'item':reportItem
                        # })
        report.update({
            'item':reportItem
        })
        # print json.dumps(reportHostName)

        # x=["System", "Title", "Status","result", "iStatus","Detail"]
        # data.append(x)

        #Put output to csv file
        # myFile=open('compl.csv','wb')
        # with myFile:
        #     writer = csv.writer(myFile)
        #     writer.writerows(data)
        #     for x in range (0,len(reportHostName)):
        #         for y in range (0,len(reportHostName[x])):
        #             writer.writerow([
        #                             reportHostName[x][y]["system"],
        #                             reportHostName[x][y]["title"],
        #                             reportHostName[x][y]["status"],
        #                             reportHostName[x][y]["result"],
        #                             reportHostName[x][y]["iStatus"],
        #                             reportHostName[x][y]["detail"],
        #                         ])


       
        # f = csv.writer(open("compl.csv", "wb+"))

        # f.writerow(["System", "Title", "Status","result", "iStatus","Detail"])

        # for x in range (0,len(reportHostName)):
        #     for y in range (0,len(reportHostName[x])):
        #         f.writerow([reportHostName[x][y]["system"],
        #                     reportHostName[x][y]["title"],
        #                     reportHostName[x][y]["status"],
        #                     reportHostName[x][y]["result"],
        #                     reportHostName[x][y]["iStatus"],
        #                     reportHostName[x][y]["detail"],
        #                     ])
        # return writer
        Jsondata=json.dumps(report)
        headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
        r=req.post(api_url,data=Jsondata,headers=headers)
        print r
        return Jsondata



def readComp():
    get_url='http://localhost:3000/compliances'
    readData = req.get(get_url)
    return readData