from flask import Flask,render_template,request,session,redirect,jsonify,url_for

# import pymysql.cursors
import hashlib
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='pulmacare',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor,
#                              autocommit=True)

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/register",methods = ['POST','GET'])
# def signup():
#     if request.method == 'GET':
#         return render_template("register.html")
#     #role 1 for hospital,2 for  patient,3 for docs
#     data=request.get_json()
#     print(data)
#     with connection.cursor() as cursor:
#         robj= dict()
#         robj['success']=False
#         try:
#             phash=hashlib.md5(data['password'].encode())
#             phash=phash.hexdigest()
#             print(phash)
#             role=data['role']
#             cursor.execute("insert into users (name,email,password,role) values(%s,%s,%s,%s)",(data['name'], data['email'],phash,data['role']))
#             if role==1:
#                 #hospital
#                 pass
#             elif role==2:
#                 #patient
#                 pass
#             else:
#                 #doctor
#                 pass

#             robj['success']=True
            
#         finally:
#             return jsonify(robj)

    

if __name__=="__main__":
    app.run(use_reloader=True, debug=True)