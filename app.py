import hashlib
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.petdiary

# 로그인 상태 관련 변수 선언
login_state = 0

# 첫 페이지 (로그인 페이지)
@app.route('/')
def home():
    # 로그인 활성
    if login_state:
        return render_template('base.html')
    # 로그인 미활성
    else:
        return render_template('login.html')

# 로그인 api
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['user_id']
    password_receive = request.form['password']

    # password 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.member.find_one({'user_id' : id_receive, 'password' : password_hash})
    print(result)

    if result is not None:
        return jsonify({'result':'success'})
    else:
        return jsonify({'fail': '아이디 또는 비밀번호가 일치하지 않습니다.'})

# 회원가입 페이지
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

# 회원가입 api
@app.route('/sign_up/save', methods=['POST'])
def sign_up_api():
    id_receive = request.form['user_id']
    password_receive = request.form['password']
    # password 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    name_receive = request.form['name']

    print(id_receive, password_receive, password_hash, name_receive)

    doc = {
        'user_id' : id_receive,
        'password' : password_hash,
        'name' : name_receive
    }
    db.member.insert_one(doc)
    return jsonify({'result':'success'})

# TODO 회원가입시 아이디 중복 체크

# 다이어리 보기 페이지
@app.route('/diary')
def diary():
    return render_template('diary.html')

# 다이어리 작성 페이지
@app.route('/diary/post')
def diary_post():
    return render_template('post.html')

# 다이어리 작성 api
@app.route('/diary/post', methods=['POST'])
def diary_post_api():

    title = request.form['title']
    content = request.form['content']

    image_type = ['JPG', 'jpg', 'PNG', 'png', 'jpeg']

    image = request.files['image']

    today = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    extension = image.filename.split('.')[-1]

    if extension not in image_type:
        return jsonify({'result': 'False', 'msg': '올바른 파일 형식이 아닙니다.'})
    filename = f'file-{today}'
    save_to = f'static/img/{filename}.{extension}'
    image.save(save_to)
    doc = {
        'title': title,
        'content': content,
        'image': f'{filename}.{extension}'
    }
    db.diary.insert_one(doc)

    return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
