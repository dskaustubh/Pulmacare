from flask import Flask,render_template,request,session,redirect
import hashlib
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

if __name__=="__main__":
    app.run(debug=True)