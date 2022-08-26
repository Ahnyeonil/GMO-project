# 패키지 설치 -> flask, pymongo, dnspython, bs4

from flask import Flask, render_template, request, jsonify, redirect, session

# mongodb url 변경
from pymongo import MongoClient
client = MongoClient('mongodb+srv://gmo:gmo@gmo.fmwwa2z.mongodb.net/gmo?retryWrites=true&w=majority')
db = client.dbprestudy
# kyt test
app = Flask(__name__)

# ayi
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)