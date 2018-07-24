import os
from flask import Flask, request, redirect, url_for,flash,render_template,send_from_directory,Response
from testParsingVuln import *
from testParsingCompl import *
import requests as req

UPLOAD_FOLDER = 'D:/ilham/ParsingXML/data'
ALLOWED_EXTENSIONS = set([ 'nessus'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__, template_folder='template')
app._static_folder ='D:/ilham/ParsingXML/template/static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    if request.form['submit'] == 'vulnerability':
                        filename = file.filename
                        file.save(os.path.join('D:/ilham/ParsingXML/data', filename))
                        dataUpload=vuln(filename)
                        idUploadFile=dataUpload['fileId']
                        uploadData=getDataVuln(idUploadFile)
                        # variabel=data[0]
                        
                        # 
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', csvFile))
                        return redirect('http://127.0.0.1:5000/vulnerabilities?id=' + idUploadFile)
                    elif request.form['submit'] == 'compliance':
                        filename = file.filename
                        file.save(os.path.join('D:/ilham/ParsingXML/data', filename))
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', ))
                        # flash('masuk ke compl')
                        dataUploadComp=compl(filename)
                        idUploadComp=dataUploadComp['fileId']
                        uploadData=getDataComp(idUploadComp)
                        # variabel=data[0][0]["system"]
                        return redirect('http://127.0.0.1:5000/compliance?id=' + idUploadComp)
                        
        
    elif request.method=='GET':
        dataVuln=readVuln()
        dataComp=readComp()
        # data=len(dataVuln)
        # dataComp=readComp()
        
        return render_template('index.html',dataFileV=dataVuln,dataFileC=dataComp)
    
   
@app.route('/vulnerabilities', methods=['GET', 'POST'])
def vulnGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    fileVuln=getDataVuln(dataId)
    return render_template('showTableVuln.html', idFile=fileVuln)

@app.route('/downloadVuln', methods=['GET', 'POST'])
def downloadVulnAsCSV():
    idFile=request.args.get('id')
    downloadVulnCSV(idFile)
    with open(idFile+'.csv') as fp:
        fileCSV=fp.read()
    return Response(
        fileCSV,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment=true; filename=idFile.csv"})

@app.route('/compliance', methods=['GET', 'POST'])
def compGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    fileComp=getDataComp(dataId)
    return render_template('showTable.html', idFile=fileComp)

@app.route('/downloadComp', methods=['GET', 'POST'])
def downloadCompAsCSV():
    idFile=request.args.get('id')
    downloadCompCSV(idFile)
    with open(idFile+'.csv') as fp:
        fileCSV=fp.read()
    return Response(
        fileCSV,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment=true; filename=idFile.csv"})

    

if __name__ == "__main__":
    app.run(debug=True)