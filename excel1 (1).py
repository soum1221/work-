from flask import Flask, render_template, request, redirect, session, url_for, flash,jsonify,send_file
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time
import urllib.request
from datetime import datetime
# import pandas as pd

app = Flask(__name__)
app.secret_key = "12345678"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ranjana@1221"
app.config["MYSQL_DB"] = "soumydb"

mysql = MySQL(app)


UPLOAD_FOLDER = "C:/Users/HP/OneDrive/Desktop/data/Invoices"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pptx' , 'docx', '.xlsx'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM jsplogin WHERE username=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            # print(info)
            if info is not None:
                if info['username'] == username and info['password'] == password:
                    return render_template("new3.html")

            else:
                return "login unsuccessful"

    return render_template("login1.html")

@app.route('/s', methods=['GET', 'POST'])
def indexx():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM client_user WHERE username=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            # print(info)
            if info is not None:
                if info['username'] == username and info['password'] == password:
                    return render_template("new2.html")

            else:
                return "login unsuccessful"

    return render_template("login1.html")

###@app.route("/upload", methods=["POST", "GET"])
#def upload():
 #   cursor = mysql.connection.cursor()
  #  cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   # now = datetime.now()
    #if request.method == 'POST':
     #   files = request.files.getlist('files[]')
        # print(files)
      #  for file in files:
       #     if file and allowed_file(file.filename):
        #        filename = secure_filename(file.filename)
         #       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          #      cur.execute("INSERT INTO images (file_name, uploaded_on) VALUES (%s, %s)", [filename, now])
           #     mysql.connection.commit()
            #print(file)
        #cur.close()
        #flash('File(s) successfully uploaded')
    #return render_template('new3.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    if request.method == 'POST':
        file = request.files['xlsx-file']
        f_path = time.ctime()
        t_obj = time.strptime(f_path)
        form_t = time.strftime("%Y%m%d%H%M%S", t_obj)
        extension = ".xlsx"
        filepath = os.path.join("C:/Users/HP/OneDrive/Desktop/excel_uploads",form_t+extension)
        file.save(filepath)
        cur.execute("INSERT INTO excel (file_name, uploaded_on) VALUES (%s, %s)", [form_t+extension, now])
        mysql.connection.commit()
        # return 'The file name of the uploaded file is: {}'.format(form_t)
    flash('File(s) successfully uploaded')
    return render_template('new3.html')


# @app.route('/connection', methods=['GET', 'POST'])
# def connection():
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST':
#         cur.execute("SELECT file_name FROM excel ORDER BY id DESC LIMIT 1;")
#         myresult = cur.fetchall()
#         myresultt=str(myresult)[16:-4]
#         print(myresultt)
#
#         cur.execute("SELECT file_name FROM images ORDER BY id DESC LIMIT 1;")
#         myresult1 = cur.fetchall()
#         myresultt1=str(myresult1)[16:-4]
#
#         print(myresultt1)
#
#         return render_template('new1.html')


@app.route('/download',methods=['GET', 'POST'])
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cur.execute("SELECT file_name FROM excel ORDER BY id DESC LIMIT 1;")
        myresultt = cur.fetchall()
        myresultt = str(myresultt)[16:-4]
        print(myresultt)
    path = "C:\\Users\\HP\\OneDrive\\Desktop\\excel_uploads\\%s"%myresultt
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(port=7000,debug=True)
