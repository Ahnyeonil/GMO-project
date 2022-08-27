# 패키지 설치 -> flask, pymongo, dnspython, bs4
import os
import random
import string
import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, jsonify, redirect, session

# mongodb url 변경

from pymongo import MongoClient
from werkzeug.utils import secure_filename

client = MongoClient('mongodb+srv://gmo:gmo@gmo.fmwwa2z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbgmo

app = Flask(__name__)


# ayi
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/gangneung/intro", methods=["POST", "GET"])
def intro_gangneung():

    return render_template("gangneung/intro.html")


@app.route("/gangneung/intro/list", methods=["GET"])
def intro_gangneung_list_send():
    # 해당 url 페이지 보안 문제로 header 값 때문에 데이터를 못받아 오는 경우가 생겨서 변경
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36'}
    data = requests.get('https://kr.hotels.com/go/south-korea/kr-best-gangneung-things-to-do', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    locations = soup.select(
        '#main-content > div > div.body-wrap.listicle-page > div.row.listicle-body > div.wrap01.col-12.col-l8 > div > '
        'div.listicle-item-wrap > div')
    locationlist = []

    for location in locations:
        a = location.select_one('div > div.header-wrap > div.header-inner-wrap > h2')
        b = location.select_one('div > div.content-wrap > div.description-wrap > p')
        c = location.select_one('div > div.img-wrap > div > img')
        if a is not None or b is not None or c is not None:
            title = a.text
            desc = b.text
            image = c['data-lazy-src']

            # print(title + '\n' + desc + '\n' + image + '\n')
            # 반복문 돌려가며 딕셔너리 배열로 만들기
            locationlist += [{
                'title': title,
                'desc': desc,
                'image': image
            }]

    # for i in locationlist:
    #     print(i)

    return jsonify({'locations': locationlist})


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

        success_msg = "포스팅 완료되었습니다"

        return render_template("gangneung/post.html", success_msg=success_msg)

    return render_template("gangneung/post.html")


@app.route("/post/list", methods=["POST", "GET"])
def post_list_send():

    all_post = list(db.posting.find({}, {'_id': False}))
    # print(all_post)

    return jsonify({'posts': all_post})


@app.route("/detail", methods=["POST", "GET"])
def detail():

    return render_template("gangneung/detail.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
