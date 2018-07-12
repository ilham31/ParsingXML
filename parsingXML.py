from lxml import etree
from collections import defaultdict

i=0
# j=1
vulnResult=defaultdict(dict)
f = open('10_23_67_85-mbss_6htdj9.nessus', 'r')
xml_content = f.read()
f.close()
root = etree.fromstring(xml_content)
for block in root:
    if block.tag == "Report":
        for report_host in block:
            if report_host.tag=="ReportHost":
                # print "Hostname :",report_host.attrib['name']
                Hostname = report_host.attrib['name']
                for report_item in report_host:
                    if report_item.tag=="ReportItem":
                        i=i+1
                        # print "nomor :",i
                        # print "Port/Protocol : ",report_item.attrib['svc_name'] +"/" +report_item.attrib['protocol']
                        portProtocol = report_item.attrib['svc_name'] +"/" +report_item.attrib['protocol']
                        # print portProtocol
                        vulnResult[i]["Port/Protocol"]=portProtocol
                        
                        # print "Severity : ",report_item.attrib['severity']
                        vulnResult[i]["Severity"]=report_item.attrib['severity']

                        # print "Name : ",report_item.attrib['pluginName'] + report_item.attrib['pluginID']
                        vulnResult[i]["Name"]=report_item.attrib['pluginName'] +" ("+report_item.attrib['pluginID']+")"

                        for param in report_item:
                            if param.tag=="solution":
                                # print "Solution :",param.text
                                vulnResult[i]["Solution"]=param.text

                            elif param.tag=="synopsis":
                                synopsis=param.text
                                # print "Synopsis abcd :",param.text
                                vulnResult[i]["Synopsis"]=synopsis

                            elif param.tag =="risk_factor":
                                # print "Risk level :",param.text
                                vulnResult[i]["risk_factor"]=param.text

                            elif param.tag =="description":
                                desc=param.text
                        
                        # print "Detail :\n"
                        # print "Synopsis : ",synopsis
                        # print "\n"
                        # print "Description : ",desc
                        vulnResult[i]["Detail"]=synopsis + desc
                        vulnResult[i]["Hostname"]=Hostname
                        # print "\n"
                # print "jumlah report item :", i
                



for j in range (1,len(vulnResult)+1):
    print vulnResult[j]["Name"] , j
    print "\n"
print len(vulnResult)