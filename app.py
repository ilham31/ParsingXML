import os
from flask import Flask, request, send_file, redirect, url_for,flash,render_template,send_from_directory,Response,session,jsonify
from testParsingVuln import *
from testParsingCompl import *
import requests as req
from flask_compress import Compress
import math


UPLOAD_FOLDER = 'D:/Project/XL/ParsingXML/data'
ALLOWED_EXTENSIONS = set([ 'nessus'])




app = Flask(__name__)
COMPRESS_MIMETYPES = ['text/html','text/css','application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE=500
Compress(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__, template_folder='template')
app._static_folder ='template/static'
app.secret_key = 'my super secret key'.encode('utf8')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


url='http://localhost:5000'


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
        if r.status_code == 401:
            return render_template('login.html',errorMessage=r.json(),stats=1)
        elif r.status_code == 403:
            return render_template('login.html',errorMessage=r.json(),stats=0)
        else:
            session['token'] = r.json()
            return redirect(url_for('upload_file'))
        
    
    else:
        if session.get('token') is not None:
            return redirect(url_for('upload_file'))
        else:
            
            return render_template('login.html')


@app.route('/change_password',methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password=request.form['old_password']
        new_password=request.form['psw']
        retype_password=request.form['retype_password']
        if 'token' in session :
                token = session['token']
                header = {'Authorization': '"Bearer ' +token}
                changePass={
                    'old_password':old_password,
                    'new_password':new_password
                }
                
                if new_password == retype_password:
                        r=req.patch('http://localhost:3000/users/password',headers=header,data=changePass)
                        status_code=r.status_code
                        if status_code == 401:
                            return render_template('reset_password.html',status=1,err=r.json())
                        else:
                            return redirect(url_for('upload_file'))
                       
                else:
                    return render_template('reset_password.html',status=0)
        else:
            return redirect (url_for('proses_user'))
    else:
        return render_template('reset_password.html')

@app.route('/manage_user',methods=['GET', 'POST'])
def manage_user():
    if session.get('token') is not None:
        token=session['token']
        header = {'Authorization': 'Bearer ' +token}
        r = req.get('http://localhost:3000/users',headers=header)
        dataUser=r.json()
        if dataUser['privilege']=='admin':
            getUser=req.get('http://localhost:3000/users/status',headers=header)
            return render_template('manageuser.html',data=getUser.json(),Users=dataUser)
        else:
            return redirect(url_for('upload_file'))
    else:
        return redirect(url_for('proses_user'))
    
@app.route('/approve_user',methods=['GET', 'POST'])
def approve_user():
    select = request.form.get('role')
    idUser=request.args.get('id')
    token=session['token']
    
    data={
        'privilege':select,
        'idUser':idUser
    }
    header = {'Authorization': 'Bearer ' +token}
    r=req.patch('http://localhost:3000/users/edit',headers=header,data=data)
    return redirect(url_for('manage_user'))

@app.route('/deny_user',methods=['GET', 'POST'])
def deny_user():
    idUser=request.args.get('id')
    token=session['token']
    header = {'Authorization': 'Bearer ' +token}
    r=req.delete('http://localhost:3000/users/delete/'+idUser,headers=header)
    return redirect(url_for('manage_user'))

@app.route('/vulnerabilities', methods=['GET', 'POST'])
def vulnGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    token = session['token']
    hal=request.args.get('page')
    fileVuln=getDataVuln(dataId,token,hal)
    sumPage=fileVuln['total_item']/100.0
    count=math.ceil(sumPage)
    pages=int(count)
    if session.get('token') is not None:
        token=session['token']
        header = {'Authorization': 'Bearer ' +token}
        r = req.get('http://localhost:3000/users',headers=header)
        dataUser=r.json()
        if dataUser["privilege"]=="admin": 
            status=1
            return render_template('showTableVuln.html', idFile=fileVuln,statusUser=status,data=dataUser,page=pages)
        else:
            status=0
            return render_template('showTableVuln.html', idFile=fileVuln,statusUser=status,data=dataUser,page=pages)
    else:
        return render_template('login.html')
        
@app.route('/downloadVuln', methods=['GET', 'POST'])
def downloadVuln():
    idFile=request.args.get('id')
    token = session['token']
    downloadVulnXLSX(idFile,token)
    return send_file('data/csv/'+idFile+'.xlsx',
                    #  mimetype='text/csv',
                     attachment_filename='vulnerabilities_'+idFile+'.xlsx',
                     as_attachment=True)

@app.route('/compliance', methods=['GET', 'POST'])
def compGet():
    selectedID = request.args.get('id')
    dataId=selectedID
    token = session['token']
    hal=request.args.get('page')
    fileComp=getDataComp(dataId,token,hal)
    sumPage=fileComp['total_item']/100.0
    count=math.ceil(sumPage)
    pages=int(count)
    if session.get('token') is not None:
        token=session['token']
        header = {'Authorization': 'Bearer ' +token}
        r = req.get('http://localhost:3000/users',headers=header)
        dataUser=r.json()
        if dataUser["privilege"]=="admin": 
            status=1
            return render_template('showTableComp.html', idFile=fileComp,statusUser=status,data=dataUser,page=pages,active=hal)
        else:
            status=0
            return render_template('showTableComp.html', idFile=fileComp,statusUser=status,data=dataUser,page=pages,active=hal)
    else:
        return render_template('login.html')

@app.route('/downloadComp', methods=['GET', 'POST'])
def downloadComp():
    idFile=request.args.get('id')
    token = session['token']
    downloadCompXLSX(idFile,token)
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
                        file.save(os.path.join('D:/Project/XL/ParsingXML/data', filename))
                        dataUpload=vuln(filename,token)
                        idUploadFile=dataUpload['fileId']
                        uploadData=getDataVuln(idUploadFile,token,hal=1)
                        # variabel=data[0]
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', csvFile))
                        return redirect(url+'/vulnerabilities?id=' + idUploadFile)
                    elif request.form['submit'] == 'compliance':
                        token = session['token']
                        filename = file.filename
                        file.save(os.path.join('D:/Project/XL/ParsingXML/data', filename))
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', ))
                        # flash('masuk ke compl')
                        dataUploadComp=compl(filename,token)
                        idUploadComp=dataUploadComp['fileId']
                        uploadData=getDataComp(idUploadComp,token,hal=1)
                        # variabel=data[0][0]["system"]
                        return redirect(url+'/compliance?id=' + idUploadComp)
                        
        
    elif request.method=='GET':
        
        if 'token' in session :
            token = session['token']
            dataVuln=readVuln(token)
            dataComp=readComp(token)
            header = {'Authorization': '"Bearer ' +token}
            r = req.get('http://localhost:3000/users',headers=header)
            dataUser=r.json()
            return render_template('index.html',dataFileV=dataVuln,dataFileC=dataComp,data=dataUser)
            
        else :
            return redirect (url_for('proses_user'))

@app.route('/editVuln', methods=['GET', 'POST'])
def close_vuln():
    selectedID = request.form['idItem']
    # idFile=request.args.get('idFile')
    token=session['token']
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    patch_Vuln='http://localhost:3000/vulnerabilities/'+ selectedID
    r = req.patch(patch_Vuln,headers=headers)
    return jsonify({'message':'success'})

# @app.route('/showVuln', methods=['GET', 'POST'])
# def close_vuln():
#     selectedID = request.form['idItem']
#     # idFile=request.args.get('idFile')
#     token=session['token']
#     headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
#     patch_Vuln='http://localhost:3000/vulnerabilities/'+ selectedID
#     r = req.get(patch_Vuln,headers=headers)
#     return jsonify({'message':'success'})

@app.route('/editComp', methods=['GET', 'POST'])
def close_comp():
    selectedID = request.form['idItem']
    # idFile=request.args.get('idFile')
    token=session['token']
    headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
    patch_Vuln='http://localhost:3000/compliance/'+ selectedID
    r = req.patch(patch_Vuln,headers=headers)
    return jsonify({'message':'success'})          

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   # remove the username from the session if it is there
   session.pop('token', None)
   return redirect(url_for('proses_user'))

# @app.errorhandler(Exception)
# def all_exception_handler(error):
#    return render_template('505.html'), 500

@app.route('/register', methods=['GET', 'POST'])
def regist_user():
    if request.method == 'POST':
        user=request.form['username']
        passwd=request.form['psw']
        userData={
                'username':user,
                'password':passwd,
            }
        r=req.post('http://localhost:3000/users',data=userData)
        status_code=r.status_code
        if status_code == 409:
            return render_template('register.html',err=r.json(),stats=1)
        else :
            return redirect(url_for('proses_user'))
    else:
        return render_template('register.html')

@app.route('/registerAdmin', methods=['GET', 'POST'])
def regist_admin():
    if request.method == 'POST':
        user=request.form['username']
        passwd=request.form['pass']
        userData={
                'username':user,
                'password':passwd,
                'privilege':"admin"
            }
        r=req.post('http://localhost:3000/users',data=userData)
        return redirect(url_for('upload_file'))
    else:
        return render_template('registerAdmin.html')

@app.route('/deletevuln', methods=['GET', 'POST'])
def deleteVuln():
   selectedID = request.form['id']
   token=session['token']
   headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
   url='http://localhost:3000/vulnerabilities/'+selectedID
   r=req.delete(url,headers=headers)
   return redirect(url_for('upload_file'))


@app.route('/deletecomp', methods=['GET', 'POST'])
def deleteComp():
   selectedID = request.args.get('id')
   token=session['token']
   headers = {'Content-Type': 'application/json', 'Accept':'application/json','Authorization':'Bearer ' + token}
   url='http://localhost:3000/compliance/'+selectedID
   r=req.delete(url,headers=headers)
   return redirect(url_for('upload_file'))


if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True)