# 패키지 설치 -> flask, pymongo, dnspython, bs4
import os
import random
import string
<<<<<<< HEAD
import requests
=======
>>>>>>> 0b83f04e544643c2ef9f5832b448a4912e8bdc10

from flask import Flask, render_template, request, jsonify, redirect, session
from bs4 import BeautifulSoup

# mongodb url 변경

from pymongo import MongoClient
from werkzeug.utils import secure_filename

client = MongoClient('mongodb+srv://gmo:gmo@gmo.fmwwa2z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbgmo

app = Flask(__name__)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://kr.hotels.com/go/south-korea/kr-best-sokcho-things-to-do')
soup = BeautifulSoup(data.text, 'html.parser')

# ayi
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sokcho/intro", methods=["POST", "GET"])
def intro_sokcho():
    return render_template("/sokcho/intro.html")

<<<<<<< HEAD
@app.route("/sokcho/postPage", methods=["POST", "GET"])
def post_sokcho():
    if request.method == 'GET':
        return render_template("/sokcho/postPage.html")
    elif request.method == 'POST':
        return jsonify({'msg': '포스트 요청을 받았습니다.'})
=======
@app.route("/gangneung/intro", methods=["POST", "GET"])
def intro_gangneung():
    return render_template("gangneung/intro.html")


@app.route("/post", methods=["POST", "GET"])
def post():
    # 포스팅 작성 기능 (form enctype 처리법을 몰라서 ajax 없이 form에서 바로 요청 됩니다)
    if request.method == 'POST':

        # file은 request.files로 받아 옵니다
        title_receive = request.form['title']
        desc_receive = request.form['desc']
        writerid_receive = request.form['writerid']
        star_receive = request.form['star']
        file_receive = request.files['file']

        path = "./static/images/"

        # 파일 이름에 랜덤 문자열 삽입
        length_of_string = 8
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        receive_filename = file_receive.filename
        index_temp = receive_filename.find(".")
        filename = receive_filename[:index_temp] + random_string + receive_filename[index_temp:]

        # 이미지 업로드 경로가 존재 하지 않을 경우 생성
        if not os.path.exists(path):
            os.mkdir(path)

        # 설정한 저장 경로에 파일 이름으로 저장
        file_receive.save(path + filename)

        # DB에 보낼 데이터 dict 저장
        doc = {
            'title': title_receive,
            'desc': desc_receive,
            'writerid': writerid_receive,
            'star': int(star_receive),
            'file': filename
        }
        
        # DB에 저장
        db.posting.insert_one(doc)

        return render_template("gangneung/post.html")

    return render_template("gangneung/post.html")
>>>>>>> 0b83f04e544643c2ef9f5832b448a4912e8bdc10


@app.route("/sokcho/detail", methods=["POST", "GET"])
def detail_sokcho():
    return render_template("detail.html")


@app.route("/gangneung/intro", methods=["POST", "GET"])
def intro_gangneung():
    return render_template("gangneung/intro.html")


@app.route("/post", methods=["POST", "GET"])
def post():
    # 포스팅 작성 기능 (form enctype 처리법을 몰라서 ajax 없이 form에서 바로 요청 됩니다)
    if request.method == 'POST':

        # file은 request.files로 받아 옵니다
        title_receive = request.form['title']
        desc_receive = request.form['desc']
        writerid_receive = request.form['writerid']
        star_receive = request.form['star']
        file_receive = request.files['file']

        path = "./static/images/"

        # 파일 이름에 랜덤 문자열 삽입
        length_of_string = 8
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        receive_filename = file_receive.filename
        index_temp = receive_filename.find(".")
        filename = receive_filename[:index_temp] + random_string + receive_filename[index_temp:]

        # 이미지 업로드 경로가 존재 하지 않을 경우 생성
        if not os.path.exists(path):
            os.mkdir(path)

        # 설정한 저장 경로에 파일 이름으로 저장
        file_receive.save(path + filename)

        # DB에 보낼 데이터 dict 저장
        doc = {
            'title': title_receive,
            'desc': desc_receive,
            'writerid': writerid_receive,
            'star': int(star_receive),
            'file': filename
        }

        # DB에 저장
        db.posting.insert_one(doc)

        return render_template("gangneung/post.html")

    return render_template("gangneung/post.html")


@app.route("/detail", methods=["POST", "GET"])
def detail():
    return render_template("gangneung/detail.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
