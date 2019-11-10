from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
import os
import numpy as np
import pandas as pd
import tensorflow as tf
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
        filename="static/pro_pics/"+filename
        file.save(filename)
        password=request.form['sgn_psw']
        name=request.form['name']
        email=request.form['sgn_email']
        phash=hashlib.md5(password.encode())
        phash=phash.hexdigest()
        role=request.form['role']
        print(role)
        try:
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
        flash("Error in the email address provided")    
    if(len(psw)<6):
        flash("Password should be atleast 6 characters long")
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
                flash("Login unsuccerssful")
                return redirect(url_for('login_page'))
        else:
            flash("Login unsuccerssful")
            return redirect(url_for('login_page'))
@app.route("/hosdash")
def hosdash():
    with connection.cursor() as cursor:
        cursor.execute("select p_id,patients.u_id,name from patients,users where h_id=%s and users.u_id=patients.u_id",str(session['h_id']))
        res=cursor.fetchall()
        print(res)
    return render_template("hospitals.html",res=res)


@app.route("/docdash")
def docdash():
    with connection.cursor() as cursor:
        cursor.execute("select p_id,stage,predict,x_id from xrays order by stage desc")
        res1=cursor.fetchall()
        res=[]
        for x in res1:
            sql_req="select name,pic_url from users,patients where p_id="+str(x['p_id'])+" and users.u_id=patients.u_id"
            cursor.execute(sql_req)
            rpl=cursor.fetchone()
            rk=dict()
            rk['name']=rpl['name']
            rk['pic_url']=rpl['pic_url']
            rk['stage']=x['stage']
            rk['x_id']=x['x_id']
            rk['predict']=(1-float(x['predict']))*100
            res.append(rk)
        print(res)
    return render_template("doctor.html",ps=res)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/uploadxray",methods=['POST'])
def uploadxray():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filename="static/xrays/"+filename
    file.save(filename)
    #pred=predict.prediction()
    model = tf.keras.models.load_model('model.h5')
    img = image.load_img(filename,target_size=(100,100))#Pneumonia Image 
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x/255.0
    pred=model.predict_proba(x)
    print(pred[0])
    eden=str(pred[0])
    eden=eden.split(' ')[0]
    hazard=eden[1:]
    hazard=float(hazard)
    stage=0
    if(hazard<.1):
        stage=3
    elif(hazard<.25):
        stage=2
    elif(hazard<.4):
        stage=1
    p_id=request.form['pato']

    with connection.cursor() as cursor:
        cursor.execute("insert into xrays(h_id,p_id,xray_url,predict,stage) values(%s,%s,%s,%s,%s)",(str(session['h_id']),str(p_id),filename,hazard,stage))
        flash("Upload sucessful")
    return redirect(url_for('hosdash'))


@app.route("/doctor_report/<string:x_id>")
def doc_report(x_id):
    with connection.cursor() as cursor:
        sql_req="select * from xrays where x_id="+str(x_id)
        session['x_id']=x_id
        cursor.execute(sql_req)
        res1=cursor.fetchone()
        print(res1)
        sql_req="select u_id from patients where p_id="+str(res1['p_id']) 
        cursor.execute(sql_req)
        res2=cursor.fetchone()
        u_id=res2['u_id']
        sql_req="select name from users where u_id="+str(u_id)
        cursor.execute(sql_req)
        res2=cursor.fetchone()
        res1['name']=res2['name']

    return render_template("doctor_report.html",x=res1)

@app.route("/post_pres",methods = ['POST'])
def post_pres():
    prescription = request.form.get("prescription")
    support = request.form.get("support")
    print(prescription)
    print(support)
    with connection.cursor() as cursor:
        cursor.execute("insert into reports (prescription,support,d_id,x_id) values(%s,%s,%s,%s)",(prescription,support,str(session['d_id']),str(session['x_id'])))
        session['x_id']=''
    return redirect(url_for('docdash'))
@app.route("/patdash")
def patdash():
    with connection.cursor() as cursor:
        cursor.execute("select * from xrays where p_id=%s",str(session['p_id']))
        res=cursor.fetchall()
        cursor.execute("select x_id from reports")
        xs=[]
        xpq=cursor.fetchall()
        x_ids=[x['x_id']for x in xpq]
        print(x_ids) 
        for r in res:
            if r['x_id'] in x_ids:
                xs.append(r)
        print(xs)     
        return render_template("patient.html",xs=res)
@app.route("/report_pat/<string:x_id>")
def report_dat(x_id):
    return (x_id)

if __name__=="__main__":
    app.run(debug=True,threaded=False)