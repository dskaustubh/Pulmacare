from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash

import pymysql.cursors
import hashlib
import os
from werkzeug.utils import secure_filename
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Login and sign up form data
name=""
email=""
psw=""
conf_psw=""

UPLOAD_FOLDER = '/static/pro_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='pulmacare',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/register",methods = ['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template("register.html")
    #role 1 for hospital,2 for  patient,3 for docs

    with connection.cursor() as cursor:
        robj= dict()
        robj['success']=False
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename="pro_pics/"+filename
        file.save(filename)
        password=request.form['password']
        name=request.form['name']
        email=request.form['email']
        phash=hashlib.md5(password.encode())
        phash=phash.hexdigest()
        role=request.form['role']
        try:


            location=request.form['location']
            print(location)
            print("je")
            cursor.execute("insert into users (name,email,password,role,pic_url,location) values(%s,%s,%s,%s,%s,%s)",(name,email,phash,role,filename,location))
            if role==1:
                #hospital
                pass
            elif role==2:
                #patient
                pass
            else:
                #doctor
                pass

            robj['success']=True
            
        finally:
            return jsonify(robj)


@app.route("/login",methods = ['POST'])
def login():
    #check if logged in
    if session['loggedin']:
        if session['role']==1:
            #role 1 for hospital,2 for  patient,3 for docs
            pass
        elif session['role']==2:
            pass
        else:
            pass
    #validation!
    flag=0
    email = request.form['log_email']
    psw = request.form['log_psw']
    if(email.find('@')==-1):
        flag=1
        flash("Error in the email address provided")    
    if(len(psw)<6):
        flag=1
        flash("Password should be atleast 6 characters long")
    if(flag==0):
        flash("Form submitted")
        return redirect(url_for('index'))
    # validation end 
    data=request.get_json()
    print(data)
    email=data['email']
    password=data['password']
    phash=hashlib.md5(password.encode())
    phash=phash.hexdigest()
    print(phash)
    with connection.cursor() as cursor:
        cursor.execute("select * from users where email=%s",email)
        myresult = cursor.fetchone()
        if(myresult):
            if(phash==myresult['password']):
                myresult['success']=True
                #init the session variables
                session['name']=myresult['name']
                session['role']=myresult['role']
                session['loggedin']=True
            else:
                myresult['success']=False
        else:
            myresult=dict()
            myresult['success']=False
        return jsonify(myresult)
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)