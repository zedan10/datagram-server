import os
from mongoengine import connect
from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from creds import admin
from werkzeug.utils import secure_filename
from csv_storage_client import CSVStorageClient

ALLOWED_EXTENSIONS = set(['csv'])

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.join(application.root_path, 'csv-files')
auth = HTTPBasicAuth()
connect(db="datagram_db")

csv_storage_client = CSVStorageClient()

@auth.get_password
def get_pw(username):
    if username in admin:
        return admin.get(username)
    return None

@application.route('/')
def test_status():
    return jsonify({'Status': 'Online'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/admin/upload/csv/', methods=['GET', 'POST'])
@auth.login_required
def upload_csv():
    error = None
    response = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = "Error! No file included to upload!"

        if 'business_name' not in request.form:
            error = "Error! Please include a business name associated with this file"

        if 'file_summary' not in request.form:
            error = "Error! Please include a brief summary for this file"

        file = request.files['file']
        if file.filename == '':
            error = "Error! No image file was selected!"

        business_name = request.form['business_name']
        file_summary = request.form['file_summary']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            res = csv_storage_client.add_csv(business_name, filename, file_summary)
            
            if isinstance(res, dict):
                response = res
            else:
                error = res
    
    return render_template('upload_csv.html', error=error, response=response)

@application.route('/admin/csv/all/', methods=['GET', 'POST'])
@auth.login_required
def get_all_uploaded_csv_files():
    error = None
    response = None
        
@application.route('/csv/<csvpath>')
def get_csv(csvpath):
    return(send_from_directory(directory='csv-files', filename=csvpath))

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')

        