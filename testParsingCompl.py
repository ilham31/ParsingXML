from lxml import etree
import os
from collections import defaultdict
import csv,json,requests as req
import xlsxwriter

def compl(filename,token):
    os.chdir('D:/Project/XL/ParsingXML/data')
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
                                'stats': status,
                                'result': result,
                                'detail': detail,
                                'i_status':iStatus,
                            })
                    # reportHostName.append({
                    #     'item':reportItem
                    # })
    report.update({
        'name':filename,
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
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    r=req.post(api_url,data=Jsondata,headers=headers)
    print r
    return r.json()


def getDataComp(idComp):
    url_data='http://localhost:3000/compliance/comp'
    parameter={'id':idComp}
    dataFile=req.get(url_data,params=parameter)
    return dataFile.json()

def readComp():
    get_url='http://localhost:3000/compliance'
    readData = req.get(get_url)
    fileComp=readData.json()
    
    return fileComp

def downloadCompCSV(idFile):
    os.chdir('D:/Project/XL/ParsingXML/data/csv')
    find_data='http://localhost:3000/compliance/comp'
    parameterDownload={'id':idFile}
    dataFile=req.get(find_data,params=parameterDownload)
    dataDownload = dataFile.json()
    
    
    workbook = xlsxwriter.Workbook('COMPLIANCE.xlsx')
    worksheet = workbook.add_worksheet()

    row=1
    col=0

    head = ['System', 'Title', 'Status', 'Result', 'i Status', 'Detail', 'Open Date', 'Closed Date', 'Status']
    for i in range (0,len(head)):
        worksheet.write(0, i, head[i])
        
    for x in range(0,len(dataDownload['item'])):
        worksheet.write(row, col, dataDownload['item'][x]["result"])
        worksheet.write(row, col + 1, dataDownload['item'][x]["i_status"])
        row += 1

    workbook.close()

    # with open(idFile+'.csv', 'wb') as csvfile:
    #     f = csv.writer(csvfile)

    #     f.writerow(["System", "Title", "Status", "result", "iStatus","Detail","Open Date","Closed Date","Status"])

    #     for x in range(0,len(dataDownload['item'])):
    #          f.writerow([dataDownload['item'][x]["system"],
    #                     dataDownload['item'][x]["title"],
    #                     dataDownload['item'][x]["stats"],
    #                     dataDownload['item'][x]["result"],
    #                     dataDownload['item'][x]["i_status"],
    #                     dataDownload['item'][x]["detail"],
    #                     dataDownload['item'][x]["open_date"],
    #                     dataDownload['item'][x]["closed_date"],
    #                     dataDownload['item'][x]["status"],
    #                     ])
    #     return f
