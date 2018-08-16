from lxml import etree

i=0
report = {}
reportHostName = []
reportItem = []
# data =[]
f = open('1 hostname comp.nessus', 'r')
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
                        title=None
                        iStatus=None
                        status=None
                        desc=None
                        iStatus=report_item.attrib['severity']
                        for param in report_item:
                            if param.tag=="{http://www.nessus.org/cm}compliance-check-name":
                                title=param.text
                            elif param.tag=="{http://www.nessus.org/cm}compliance-result":
                                status=param.text
                            elif param.tag =="description":
                                desc=param.text
                                
                                
                        reportItem.append({
                            'system': System,
                            'title': title,
                            'stats': status,
                            'result': desc,
                            'detail': desc,
                            'i_status':iStatus,
                        })
                # reportHostName.append({
                #     'item':reportItem
                # })
report.update({
    
    'item':reportItem,
    
})
# print json.dumps(reportHostName)
print len(reportItem)
    