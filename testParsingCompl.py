from lxml import etree
import os
from collections import defaultdict
import csv,json,requests as req
import xlsxwriter

path = 'D:/ilham/ParsingXML/data'

def compl(filename,token):
    os.chdir(path)
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


def getDataComp(idComp,token):
    url_data='http://localhost:3000/compliance/comp'
    parameter={'id':idComp}
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    dataFile=req.get(url_data,params=parameter,headers=headers)
    return dataFile.json()

def readComp(token):
    get_url='http://localhost:3000/compliance'
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    readData = req.get(get_url,headers=headers)
    fileComp=readData.json()
    
    return fileComp

def downloadCompXLSX(idFile,token):
    os.chdir(path+'/csv')
    find_data='http://localhost:3000/compliance/comp'
    parameterDownload={'id':idFile}
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
   
    dataFile=req.get(find_data,params=parameterDownload,headers=headers)
    dataDownload = dataFile.json()
    
    
    workbook = xlsxwriter.Workbook(idFile +'.xlsx')
    worksheet = workbook.add_worksheet()
    
    green_format = workbook.add_format()
    green_format.set_pattern(1)
    green_format.set_bg_color('green')
    green_format.set_font_color('white')

    yellow_format = workbook.add_format()
    yellow_format.set_pattern(1)
    yellow_format.set_bg_color('yellow')
    yellow_format.set_font_color('white')

    red_format = workbook.add_format()
    red_format.set_pattern(1)
    red_format.set_bg_color('red')
    red_format.set_font_color('white')

    row=1
    col=0

    head = ['System', 'Title', 'Status', 'Result', 'i Status', 'Detail', 'Open Date', 'Closed Date', 'Status']
    for i in range (0,len(head)):
        worksheet.write(0, i, head[i])
        
    for x in range(0,len(dataDownload['item'])):
        worksheet.write(row, 0, dataDownload['item'][x]["system"])
        worksheet.write(row, 1, dataDownload['item'][x]["title"])
        if dataDownload['item'][x]['stats']== 'PASSED':
            worksheet.write(row, 2, dataDownload['item'][x]["stats"],green_format)
        elif dataDownload['item'][x]['stats']== 'WARNING' :
            worksheet.write(row, 2, dataDownload['item'][x]["stats"],yellow_format)
        else:
            worksheet.write(row, 2, dataDownload['item'][x]["stats"],red_format)
        worksheet.write(row, 3, dataDownload['item'][x]["result"])
        worksheet.write(row, 4, dataDownload['item'][x]["i_status"])
        worksheet.write(row, 5, dataDownload['item'][x]["detail"])
        worksheet.write(row, 6, dataDownload['item'][x]["open_date"])
        worksheet.write(row, 7, dataDownload['item'][x]["closed_date"])
        worksheet.write(row, 8, dataDownload['item'][x]["status"])
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
