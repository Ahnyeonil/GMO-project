# 패키지 설치 -> flask, pymongo, dnspython, bs4
import os
import random
import string
import requests

from flask import Flask, render_template, request, jsonify, redirect, session
from bs4 import BeautifulSoup

from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.utils import secure_filename

# mongodb url 변경
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
            'title': title,
            'tag': tag,
            'desc': desc,
            'link': 'https://map.naver.com/v5/search/' + title + '/place'
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
        city_receive = request.form['city_give']
        dst_receive = request.form['dst_give']
        star_receive = request.form['star_give']
        title_receive = request.form['title_give']
        dsc_receive = request.form['dsc_give']

        doc = {
            'city': city_receive,
            'dst': dst_receive,
            'star': star_receive,
            'title': title_receive,
            'dsc': dsc_receive,
        }
        db.post.insert_one(doc)
        return jsonify({'msg': '등록되었습니다'})


@app.route("/gangneung/intro", methods=["POST", "GET"])
def intro_gangneung():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36'}

    data = requests.get('https://kr.hotels.com/go/south-korea/kr-best-gangneung-things-to-do', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    sights = soup.select(
        '#main-content > div > div.body-wrap.listicle-page > div.row.listicle-body > div.wrap01.col-12.col-l8 > div > div.listicle-item-wrap > div')

    travleList = []

    for sight in sights:
        sight_title = sight.select_one('div > div.header-wrap > div.header-inner-wrap > h2').text
        sight_desc = sight.select_one('div > div.content-wrap > div.description-wrap > p').text
        sight_tags = sight.select('div > div.content-wrap > div.tag-container > ul > li')

        tags = []

        for tag in sight_tags:
            tags.append(tag.text)

        travleList.append({
            'title': sight_title,
            'desc': sight_desc,
            'tag': tags
        })

    return render_template("/gangneung/intro.html", travleList=travleList)


@app.route("/post", methods=["POST", "GET"])
def post():
    # 포스팅 작성 기능 (form enctype 처리법을 몰라서 ajax 없이 form에서 바로 요청 됩니다)
    if request.method == 'POST':

        print(request.form)
        print(request.files)
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

        # POST => redirect
        return redirect("/post")

    return render_template("gangneung/post.html")


@app.route("/post/list", methods=["POST", "GET"])
def post_list_send():
    all_post = list(db.posting.find({}, {'_id': False}))

    return jsonify({'posts': all_post})


@app.route("/post/simpledetail", methods=["POST", "GET"])
def post_simpledetail_send():
    if request.method == 'POST':
        title_receive = request.form['titlename']
        titlepost = db.posting.find_one({'title': title_receive}, {'_id': False})

    return jsonify({'postdetail': titlepost})


@app.route("/detail", methods=["POST", "GET"])
def detail():
    if request.method == 'POST':
        comment_receive = request.form['comment']
        author_receive = request.form['author']
        password_receive = request.form['password']
        postingid_receive = request.form['postingid']

        doc = {
            'comment': comment_receive,
            'nickname': author_receive,
            'password': password_receive,
            'posting': postingid_receive,
        }

        db.comment.insert_one(doc)

        return redirect("/detail")

    all_post = list(db.posting.find())

    for a in all_post:
        a['_id'] = str(a['_id'])

    id_receive = '630fba7de2397ba9a399a2ef'
    default_comment = list(db.comment.find({'posting': id_receive}))
    for a in default_comment:
        a['_id'] = str(a['_id'])

    return render_template("gangneung/detail.html", postlist=all_post, default_comment_list=default_comment)


@app.route("/detail/list", methods=["POST", "GET"])
def detail_list_send():
    if request.method == 'POST':
        id_receive = request.form['idstr']

        postingfind = db.posting.find_one({'_id': ObjectId(id_receive)})
        postingfind['_id'] = str(postingfind['_id'])

        commentfind = list(db.comment.find({'posting': id_receive}))
        for a in commentfind:
            a['_id'] = str(a['_id'])

        return jsonify({'postdetail': postingfind, 'comments': commentfind, 'hiddenid': id_receive})


@app.route("/gangneung/detail/deletecomment", methods=["POST", "GET"])
def detail_comment():
    if request.method == 'POST':
        id_receive = request.form['commentid']
        pwd_receive = request.form['commentpwd']

        commentfind = db.comment.find_one({'_id': ObjectId(id_receive)})

        if commentfind is not None and commentfind['password'] == pwd_receive:
            db.comment.delete_one({'_id': ObjectId(id_receive)})
            return jsonify({"msg": "댓글 삭제 완료"})
        
        else:
            return jsonify({"msg": "비밀번호가 다릅니다"})

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

    return render_template("ayi/post.html", postinglist=postinglist)


@app.route("/ayi/detail", methods=["GET"])
def detail_ayi():
    obj = request.values['_id']

    posting = db.posting.find_one({'_id': ObjectId(obj)})
    commentlist = list(db.comment.find({'posting': obj}))

    return render_template("ayi/detail.html", posting=posting, commentlist=commentlist)


@app.route("/ayi/comment", methods=["POST"])
def comment_ayi():
    pid = request.form['pid']
    comment = request.form['comment']
    nickname = request.form['nickname']
    password = request.form['password']

    doc = {
        'comment': comment,
        'nickname': nickname,
        'password': password,
        'posting': pid
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# 속초 포스팅 추가 접속 화면
@app.route('/sokcho/posting')
def posting():
    return render_template('post.html')


# 속초 포스팅 추가 페이지(posting.html) 데이터 서버와 클라이언트 통신
@app.route("/sokcho/posting/post", methods=["POST"])
def posting_post():
    picture_receive = request.form['picture_give']
    name_receive = request.form['name_give']
    title_receive = request.form['title_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    doc = {
        'picture' : picture_receive,
        'name': name_receive,
        'title': title_receive,
        'star': star_receive,
        'comment': comment_receive
    }

    db.posting.insert_one(doc)

    return jsonify({'msg': 'POST(속초 포스팅) 연결 완료!'})

# 속초 포스팅 추가 페이지(posting.html) Get 연결
@app.route("/sokcho/posting/get", methods=["GET"])
def posting_get():
    return jsonify({'msg': 'GET 연결 완료!'})

# 속초 포스팅 리스트 페이지(PostingList.html) Get 연결
@app.route("/sokcho/postinglist/get", methods=["GET"])
def postinglist_get():
    posting_list = list(db.posting.find({}, {'_id': False}))

    return jsonify({'postings': posting_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)