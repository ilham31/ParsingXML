import os
from flask import Flask, request, redirect, url_for,flash,render_template,send_from_directory
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
                        vuln(filename)
                        # variabel=data[0]
                        
                        # 
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', csvFile))
                        return render_template('index.html')
                    elif request.form['submit'] == 'compliance':
                        filename = file.filename
                        file.save(os.path.join('D:/ilham/ParsingXML/data', filename))
                        # file.save(os.path.join('D:/project/pkl/ParsingXML/data', ))
                        # flash('masuk ke compl')
                        compl(filename)
                        # variabel=data[0][0]["system"]
                        return render_template('index.html')
        
    elif request.method=='GET':
        
        return render_template('index.html')
    
   


if __name__ == "__main__":
    app.run(debug=True)