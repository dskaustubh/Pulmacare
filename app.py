from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
import os
import predict
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
from werkzeug.utils import secure_filename
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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

@app.route("/signup_page")
def signup_page():
    return render_template('signup.html')

@app.route("/login_page")
def login_page():
    return render_template('login.html')
    
@app.route("/register",methods = ['POST'])
def signup():
    #role 1 for hospital,2 for  patient,3 for docs
    with connection.cursor() as cursor:
        robj= dict()
        robj['success']=False
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename="pro_pics/"+filename
        file.save(filename)
        password=request.form['sgn_psw']
        name=request.form['name']
        email=request.form['sgn_email']
        phash=hashlib.md5(password.encode())
        phash=phash.hexdigest()
        role=request.form['role']
        print(role)
        try:
            #location=request.form['location'] mostly not req but we will see
            cursor.execute("insert into users (name,email,password,role,pic_url) values(%s,%s,%s,%s,%s)",(name,email,phash,role,filename))
            cursor.execute("select * from users where email=%s",email)
            myresult = cursor.fetchone()
            if role=="1":
                #hospital
                cursor.execute("insert into hospitals(u_id) values(%s)",(myresult['u_id']))
            elif role=="2":
                #patient
                cursor.execute("insert into patients(u_id) values(%s)",(myresult['u_id']))
            else:
                #doctor
                cursor.execute("insert into doctors(u_id) values(%s)",(myresult['u_id']))

            robj['success']=True
            
        finally:
            return redirect(url_for("login_page"))

@app.route("/login",methods = ['POST'])
def login():
    #check if logged in
    if 'loggedin' in session:
        if session['role']==1:
            #role 1 for hospital,2 for  patient,3 for docs
            return render_template("hospitals.html")
            
        elif session['role']==2:
            return render_template("patient.html")
        else:
            return render_template("doctor.html")
    # #validation!
    # flag=0
    email = request.form['log_email']
    psw = request.form['log_psw']
    if(email.find('@')==-1):
        # flag=1
        flash("Error in the email address provided")    
    if(len(psw)<6):
        # flag=1
        flash("Password should be atleast 6 characters long")
    # if(flag==0):
    #     flash("Form submitted")
    #     return redirect(url_for('index'))
    # validation end 
    password=psw
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
                session['u_id']=myresult['u_id']
                session['name']=myresult['name']
                session['role']=myresult['role']
                session['pic_url']=myresult['pic_url']
                session['location']=myresult['location']
                session['loggedin']=True
                #role 1 for hospital,2 for  patient,3 for docs
                if(session['role']=="1"):
                    sql_req="select * from hospitals where u_id="+str(session['u_id'])
                    cursor.execute(sql_req)
                    res1=cursor.fetchone()
                    session['h_id']=res1['h_id']
                    return redirect(url_for('hosdash'))
                elif session['role']=="2":
                    cursor.execute("select * from patients where u_id=%s",str(session['u_id']))
                    res1=cursor.fetchone()
                    session['p_id']=res1['p_id']
                    #return render_template("patient.html")
                    return redirect(url_for('patdash'))
                else:
                    cursor.execute("select * from doctors where u_id=%s",str(session['u_id']))
                    res1=cursor.fetchone()
                    session['d_id']=res1['d_id']
                    return redirect(url_for('docdash'))
            else:
                myresult['success']=False
        else:
            myresult=dict()
            myresult['success']=False
        return jsonify(myresult)
@app.route("/hosdash")
def hosdash():
    with connection.cursor() as cursor:
        cursor.execute("select p_id,patients.u_id,name from patients,users where h_id=%s and users.u_id=patients.u_id",str(session['h_id']))
        res=cursor.fetchall()
        print(res)
    return render_template("hospitals.html",res=res)
@app.route("/patdash")
def patdash():
    return render_template("patient.html")
@app.route("/docdash")
def docdash():
    return render_template("doctors.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/uploadxray",methods=['POST'])
def uploadxray():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filename="xrays/"+filename
    file.save(filename)
    #pred=predict.prediction()
    model = tf.keras.models.load_model('model.h5')
    img = image.load_img('test_3.jpeg', target_size=(100,100))#Pneumonia Image 
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x/255.0
    pred=model.predict_proba(x)
    print(pred[0])
    return("hi")
    
if __name__=="__main__":
    app.run(debug=True,threaded=False)