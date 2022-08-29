# 패키지 설치 -> flask, pymongo, dnspython, bs4
import os
import random
import string
import requests

from flask import Flask, render_template, request, jsonify, redirect, session
from bs4 import BeautifulSoup

# mongodb url 변경

from pymongo import MongoClient

client = MongoClient('mongodb+srv://gmo:gmo@gmo.fmwwa2z.mongodb.net/?retryWrites=true&w=majority')
db = client.dbgmo

app = Flask(__name__)

# ayi
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sokcho/intro", methods=["POST", "GET"])
def intro_sokcho():
    locationlist = list()

    # 속초 크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36'}
    data = requests.get('https://kr.hotels.com/go/south-korea/kr-best-sokcho-things-to-do')
    soup = BeautifulSoup(data.text, 'html.parser')

    places = soup.select(
        '#main-content > div > div.body-wrap.listicle-page > div.row.listicle-body > div.wrap01.col-12.col-l8 > div > div.listicle-item-wrap > div')

    for place in places:
        title = place.select_one('div > div.header-wrap > div.header-inner-wrap').text
        desc = place.select_one('div > div.content-wrap > div.description-wrap > p').text
        tag = list()

        tags = place.select('div > div.content-wrap > div.tag-container > ul > li')
        for num in range(len(tags)):
            tag.append('#' + tags[num].text)

        locationlist.append({
            'title' : title,
            'tag' : tag,
            'desc' : desc,
            'link' : 'https://map.naver.com/v5/search/' + title + '/place'
        })

    return render_template("/sokcho/intro.html", locationlist=locationlist)

@app.route("/sokcho/detail", methods=["POST", "GET"])
def detail_sokcho():
    return render_template("detail.html")

@app.route("/sokcho/post", methods=["POST", "GET"])
def post_sokcho():
    if request.method == 'GET':
        return render_template("/sokcho/post.html")
    elif request.method == 'POST':
        return jsonify({'msg': '포스트 요청을 받았습니다.'})

@app.route("/gangneung/intro", methods=["POST", "GET"])
def intro_gangneung():

    return render_template("gangneung/intro.html")

@app.route("/gangneung/intro/list", methods=["GET"])
def intro_gangneung_list():
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
            # 반복문 돌아가며 딕셔너리 배열로 만들기
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

        return render_template("gangneung/post.html")

    return render_template("gangneung/post.html")

@app.route("/detail", methods=["POST", "GET"])
def detail():
    return render_template("gangneung/detail.html")

@app.route("/temp/tempComment", methods=["POST", "GET"])
def tempComment():
    obj = '630945ebfb79ff41c5bbda70'
#    db.comment.insert_one({'comment': '고고댓글3', 'nickname': '안철수3', 'password': '1234', 'posting': '630945ebfb79ff41c5bbda70'})
    return render_template("temp/tempComment.html", obj = obj)

@app.route("/tempHomework", methods=["GET"])
def homework_get():

    obj = request.values['obj']
    fan_list = list(db.comment.find({'posting' : obj}))

    for l in fan_list:
        l['_id'] = str(l['_id'])
    return jsonify({'fan_list' : fan_list})

@app.route("/ayi/post", methods=["POST", "GET"])
def post_ayi():
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

        return redirect("ayi/post.html")

    postinglist = list(db.posting.find())

    for p in postinglist:
        p['_id'] = str(p['_id'])

    return render_template("ayi/post.html", postinglist = postinglist)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
