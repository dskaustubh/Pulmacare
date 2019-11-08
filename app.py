from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
import os
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
    if 'loggedin' in session:
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