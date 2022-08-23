# 패키지 설치 -> flask, pymongo, dnspython, bs4

from flask import Flask, render_template, request, jsonify, redirect, session

# mongodb url 변경
from pymongo import MongoClient
client = MongoClient('mongodb+srv://ahn:sparta@cluster0.s9tldtb.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbprestudy

app = Flask(__name__)

# ayi
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)