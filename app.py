from flask import Flask,render_template,request,session,url_for,redirect
import hashlib
app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html', methods = ['GET'])

# if __name__=="__main__":
app.run(debug=True)