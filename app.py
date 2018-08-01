import os
from flask import Flask, request, send_file, redirect, url_for,flash,render_template,send_from_directory,Response,session
from testParsingVuln import *
from testParsingCompl import *
import requests as req


UPLOAD_FOLDER = 'D:/ilham/ParsingXML/data'
ALLOWED_EXTENSIONS = set([ 'nessus'])




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__, template_folder='template')
app._static_folder ='template/static'
app.secret_key = 'my super secret key'.encode('utf8')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/', methods=['GET', 'POST'])
def proses_user():
    if request.method =='POST':
        user=request.form['username']
        passwd=request.form['pass']
        userLogin={
            'username':user,
            'password':passwd
        }
        r=req.post('http://localhost:3000/users/login',data=userLogin)
        if r.json()== 'user tidak ada' or r.json() =='password tidak cocok':
            return redirect(url_for('proses_user'))
        else:
            session['token'] = r.json()
            return redirect(url_for('upload_file'))
        
    
    else:
        if session.get('token') is not None:
            return redirect(url_for('upload_file'))
        else:
            return render_template('login.html')


@app.route('/vulnerabilities', methods=['GET', 'POST'])
def vulnGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    fileVuln=getDataVuln(dataId)
    if session.get('token') is not None:
        token=session['token']
        header = {'Authorization': 'Bearer ' +token}
        r = req.get('http://localhost:3000/users',headers=header)
        dataUser=r.json()
        if dataUser["privilege"]=="admin": 
            status=1
            return render_template('showTableVuln.html', idFile=fileVuln,statusUser=status,data=dataUser)
        else:
            status=0
            return render_template('showTableVuln.html', idFile=fileVuln,statusUser=status,data=dataUser)
    else:
        return render_template('login.html')
        
@app.route('/downloadVuln', methods=['GET', 'POST'])
def downloadVuln():
    idFile=request.args.get('id')
    downloadVulnXLSX(idFile)
    return send_file('data/csv/'+idFile+'.xlsx',
                    #  mimetype='text/csv',
                     attachment_filename='vulnerabilities_'+idFile+'.xlsx',
                     as_attachment=True)

@app.route('/compliance', methods=['GET', 'POST'])
def compGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    fileComp=getDataComp(dataId)
    if session.get('token') is not None:
        token=session['token']
        header = {'Authorization': 'Bearer ' +token}
        r = req.get('http://localhost:3000/users',headers=header)
        dataUser=r.json()
        if dataUser["privilege"]=="admin": 
            status=1
            return render_template('showTableComp.html', idFile=fileComp,statusUser=status,data=dataUser)
        else:
            status=0
            return render_template('showTableComp.html', idFile=fileComp,statusUser=status,data=dataUser)
    else:
        return render_template('login.html')
@app.route('/downloadComp', methods=['GET', 'POST'])
def downloadComp():
    idFile=request.args.get('id')
    downloadCompXLSX(idFile)
    return send_file('data/csv/'+idFile+'.xlsx',
                    #  mimetype='text/csv',
                     attachment_filename='compliance '+idFile+'.xlsx',
                     as_attachment=True)

@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    # return render_template ('index.html')
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
                        token = session['token']
                        filename = file.filename
                        file.save(os.path.join('D:/ilham/ParsingXML/data', filename))
                        dataUpload=vuln(filename,token)
                        idUploadFile=dataUpload['fileId']
                        uploadData=getDataVuln(idUploadFile)
                        # variabel=data[0]
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', csvFile))
                        return redirect('http://127.0.0.1:5000/vulnerabilities?id=' + idUploadFile)
                    elif request.form['submit'] == 'compliance':
                        token = session['token']
                        filename = file.filename
                        file.save(os.path.join('D:/ilham/ParsingXML/data', filename))
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', ))
                        # flash('masuk ke compl')
                        dataUploadComp=compl(filename,token)
                        idUploadComp=dataUploadComp['fileId']
                        uploadData=getDataComp(idUploadComp)
                        # variabel=data[0][0]["system"]
                        return redirect('http://127.0.0.1:5000/compliance?id=' + idUploadComp)
                        
        
    elif request.method=='GET':
        dataVuln=readVuln()
        dataComp=readComp()
        if 'token' in session :
            token = session['token']
            header = {'Authorization': '"Bearer ' +token}
            r = req.get('http://localhost:3000/users',headers=header)
            dataUser=r.json()
            return render_template('index.html',dataFileV=dataVuln,dataFileC=dataComp,data=dataUser)
            
        else :
            return redirect (url_for('proses_user'))

@app.route('/editVuln', methods=['GET', 'POST'])
def close_vuln():
    selectedID = request.args.get('idItem')
    idFile=request.args.get('idFile')
    patch_Vuln='http://localhost:3000/vulnerabilities/'+ selectedID
    r = req.patch(patch_Vuln)
    return redirect('http://127.0.0.1:5000/vulnerabilities?id=' + idFile)

@app.route('/editComp', methods=['GET', 'POST'])
def close_comp():
    selectedID = request.args.get('idItem')
    idFile=request.args.get('idFile')
    patch_Vuln='http://localhost:3000/compliance/'+ selectedID
    r = req.patch(patch_Vuln)
    return redirect('http://127.0.0.1:5000/compliance?id=' + idFile)           

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   # remove the username from the session if it is there
   session.pop('token', None)
   return redirect(url_for('proses_user'))
# @app.errorhandler(Exception)
# def all_exception_handler(error):
#    return 'Error', 500

@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    if request.method == 'POST':
        user=request.form['username']
        passwd=request.form['pass']
        userData={
                'username':user,
                'password':passwd,
                'privilege':"user"
            }
        r=req.post('http://localhost:3000/users',data=userData)
        return redirect(url_for('proses_user'))
    else:
        return render_template('register.html')

@app.route('/deletevuln', methods=['GET', 'POST'])
def deleteVuln():
   selectedID = request.args.get('id')
   url='http://localhost:3000/vulnerabilities/'+selectedID
   r=req.delete(url)
   return redirect(url_for('upload_file'))


@app.route('/deletecomp', methods=['GET', 'POST'])
def deleteComp():
   selectedID = request.args.get('id')
   url='http://localhost:3000/compliance/'+selectedID
   r=req.delete(url)
   return redirect(url_for('upload_file'))


if __name__ == "__main__":
    app.run(debug=True)