from lxml import etree
from io import open
import json
import csv
import os,requests as req
import xlsxwriter

path = 'D:/ilham/ParsingXML/data'

def vuln(filename,token):
    os.chdir(path)
    api_url='http://localhost:3000/vulnerabilities'
    i=0
    report = {}
    reportHostName = []
    reportItem = []
    nessusFile = open(filename, 'r')
    xml_content = nessusFile.read()
    nessusFile.close()
    data=[]
    root = etree.fromstring(xml_content)
    for block in root:
        if block.tag == "Report":
            
            for report_host in block:
                if report_host.tag=="ReportHost":
                    Hostname = report_host.attrib['name']
                    # reportItem = []
                    for report_item in report_host:
                        if report_item.tag=="ReportItem":
                            portProtocol=None
                            severity=None
                            name=None
                            solution=None
                            synopsis=None
                            risk_factor=None
                            desc=None
                            detail=None
                            portProtocol = report_item.attrib['svc_name'] +"/" +report_item.attrib['protocol']
                            severity = report_item.attrib['severity']
                            name = report_item.attrib['pluginName'] +" ("+report_item.attrib['pluginID']+")"
                            for param in report_item:
                                if param.tag=="solution":
                                    solution = param.text

                                elif param.tag=="synopsis":
                                    synopsis=param.text

                                elif param.tag =="risk_factor":
                                    risk_factor=param.text

                                elif param.tag =="description":
                                    desc=param.text
                            if desc and synopsis is not None:
                                detail = synopsis + desc
                            elif desc is None:
                                detail=synopsis
                            elif synopsis is None:
                                detail=desc
                            reportItem.append({
                                'system': Hostname,
                                'name': name,
                                'severity': severity,
                                'port_protocol': portProtocol,
                                'solution': solution,
                                'synopsis': synopsis,
                                'detail': detail,
                                'risk_level': risk_factor
                            })
                    # reportHostName.append({
                    #     'item':reportItem
                    # })
    report.update({
        'name' : filename,
        'item' : reportItem
    })            

    # x=["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity"]
    # data.append(x)

#Put output to csv file
    # myFile=open('vulnv.csv','wb')
    # with myFile:
    #     writer = csv.writer(myFile)
    #     writer.writerows(data)
    #     for x in range (0,len(reportHostName)):
    #         for y in range (0,len(reportHostName[x])):
    #             writer.writerow([reportHostName[x][y]["hostname"],
    #                         reportHostName[x][y]["name"],
    #                         reportHostName[x][y]["port/protocol"],
    #                         reportHostName[x][y]["risk_level"],
    #                         reportHostName[x][y]["synopsis"],
    #                         reportHostName[x][y]["detail"],
    #                         reportHostName[x][y]["solution"],
    #                         reportHostName[x][y]["severity"],
    #                         ])
    # with open('vulnv.csv', 'wb') as csvfile:
    #     f = csv.writer(csvfile)

    #     f.writerow(["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity"])

    #     for x in range (0,len(reportHostName)):
    #         for y in range (0,len(reportHostName[x])):
    #             f.writerow([reportHostName[x][y]["hostname"],
    #                         reportHostName[x][y]["name"],
    #                         reportHostName[x][y]["port/protocol"],
    #                         reportHostName[x][y]["risk_level"],
    #                         reportHostName[x][y]["synopsis"],
    #                         reportHostName[x][y]["detail"],
    #                         reportHostName[x][y]["solution"],
    #                         reportHostName[x][y]["severity"],
    #                         ])
    

    # return f
    Jsondata=json.dumps(report)
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    r=req.post(api_url,data=Jsondata,headers=headers)
    return r.json()


def readVuln(token):
    get_url='http://localhost:3000/vulnerabilities'
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    readData = req.get(get_url,headers=headers)
    fileVuln=readData.json()
    
    return fileVuln


def getDataVuln(idVuln,token,hal):
    url_data='http://localhost:3000/vulnerabilities/vuln'
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    parameter={'id':idVuln,'page':hal}
    dataFile=req.get(url_data,params=parameter,headers=headers)
    return dataFile.json()

def downloadVulnXLSX(idFile,token):
    os.chdir(path+'/csv')
    find_data='http://localhost:3000/vulnerabilities/download'
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    parameterDownload={'id':idFile}
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

    head = ['#','System', 'Name', 'Port/Protocol', 'Risk Level', 'Synopsis', 'Detail','Solution','Severity','Open Date', 'Closed Date', 'Status']
    for i in range (0,len(head)):
        worksheet.write(0, i, head[i])
        
    for x in range(0,len(dataDownload['item'])):
        worksheet.write(row, 0, dataDownload['item'][x]["index"])
        worksheet.write(row, 1, dataDownload['item'][x]["system"])
        worksheet.write(row, 2, dataDownload['item'][x]["name"])
        worksheet.write(row, 3, dataDownload['item'][x]["port_protocol"])
        if dataDownload['item'][x]["risk_level"] == 'High':
            worksheet.write(row, 4, dataDownload['item'][x]["risk_level"],red_format)
        elif dataDownload['item'][x]["risk_level"] == 'Medium':
            worksheet.write(row, 4, dataDownload['item'][x]["risk_level"],yellow_format)
        elif dataDownload['item'][x]["risk_level"] == 'Low':
            worksheet.write(row, 4, dataDownload['item'][x]["risk_level"],green_format)
        else :
            worksheet.write(row, 4, dataDownload['item'][x]["risk_level"])
        worksheet.write(row, 5, dataDownload['item'][x]["synopsis"])
        worksheet.write(row, 6, dataDownload['item'][x]["detail"])
        worksheet.write(row, 7, dataDownload['item'][x]["solution"])
        worksheet.write(row, 8, dataDownload['item'][x]["severity"])
        worksheet.write(row, 9, dataDownload['item'][x]["open_date"])
        worksheet.write(row, 10, dataDownload['item'][x]["closed_date"])
        worksheet.write(row, 11, dataDownload['item'][x]["status"])
        row += 1

    workbook.close()
    # with open(idFile+'.csv', 'wb') as csvfile:
    #     f = csv.writer(csvfile)

    #     f.writerow(["System", "Name", "Port/Protocol", "Risk Level", "Synopsis","Detail","Solution","Severity","Open Date","Closed Date","Status"])

    #     for x in range(0,len(dataDownload['item'])):
    #          f.writerow([dataDownload['item'][x]["system"],
    #                     dataDownload['item'][x]["name"],
    #                     dataDownload['item'][x]["port_protocol"],
    #                     dataDownload['item'][x]["risk_level"],
    #                     dataDownload['item'][x]["synopsis"],
    #                     dataDownload['item'][x]["detail"],
    #                     dataDownload['item'][x]["solution"],
    #                     dataDownload['item'][x]["severity"],
    #                     dataDownload['item'][x]["open_date"],
    #                     dataDownload['item'][x]["closed_date"],
    #                     dataDownload['item'][x]["status"],
    #                     ])
    #     return f
    
