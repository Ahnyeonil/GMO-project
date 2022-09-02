from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.tndyy3u.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 속초 포스팅 리스트 접속 화면
@app.route('/')
def postingList():
    return render_template('PostingList.html')

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