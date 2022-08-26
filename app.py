# 패키지 설치 -> flask, pymongo, dnspython, bs4

from flask import Flask, render_template, request, jsonify, redirect, session

# mongodb url 변경

from pymongo import MongoClient

client = MongoClient('mongodb+srv://gmo:gmo@gmo.fmwwa2z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbgmo

app = Flask(__name__)


# ayi
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/introSokcho", methods=["POST", "GET"])
def introSokcho():
    return render_template("introSokcho.html")


@app.route("/introGangneung", methods=["POST", "GET"])
def introGangneung():
    return render_template("introGangneung.html")


@app.route("/postPage", methods=["POST", "GET"])
def post():
    if request.method == 'GET':
        return render_template("postPage.html")
    elif request.method == 'POST':
        return jsonify({'msg': '포스트 요청을 받았습니다.'})


@app.route("/detail", methods=["POST", "GET"])
def detail():
    return render_template("detail.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
