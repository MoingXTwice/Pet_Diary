import hashlib
from datetime import datetime, timedelta
import requests
import jwt

from flask import Flask, render_template, request, jsonify, flash, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

SECRET_KEY = 'PET-DIARY'

client = MongoClient('localhost', 27017)
db = client.petdiary

# 첫 페이지
@app.route('/<user_id>')
def home(user_id):
    token_receive = request.cookies.get('mytoken')
    print(user_id)
    print(token_receive)

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (user_id == payload['id'])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        member = db.member.find_one({'user_id': payload['id']})
        return render_template('main.html', member=member, status=status)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/login')

# 로그인 페이지
@app.route('/login')
def login():
    token_receive = request.cookies.get('mytoken')
    try:
        jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        flash('이미 로그인 되어 있습니다.')
        return redirect('/')
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('login.html')

# 로그인 api
@app.route('/login', methods=['POST'])
def login_api():
    id_receive = request.form['user_id']
    password_receive = request.form['password']

    # password 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.member.find_one({'user_id' : id_receive, 'password' : password_hash})
    print(result)

    if result is not None:
        #토큰 생성
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds = 60 * 60 * 24) #로그인 24시간 유지 #now 대신 utcnow 를 사용 하는 이유는 토큰 만료시간 조작?을 막기위해 #now는 클라이언트의 환경에 따라 시간이 바뀐다.
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})

# 회원가입 페이지
@app.route('/sign_up')
def sign_up():
    token_receive = request.cookies.get('mytoken')
    try:
        jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        flash('이미 로그인되어 있습니다.')
        return redirect(url_for('/'))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('sign_up.html')

# 회원가입 api
@app.route('/sign_up', methods=['POST'])
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
    return jsonify({'result': 'success'})

# TODO 회원가입시 아이디 중복 체크

# # 로그인 후 메인 페이지
# @app.route('/main')
# def main():
#     return render_template('main.html')

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

    url = "http://spartacodingclub.shop/sparta_api/weather/seoul"
    weather = requests.get(url).json()
    weather_icon = weather['icon']

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
        'image': f'{filename}.{extension}',
        'weather': weather_icon
    }
    db.diary.insert_one(doc)

    return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
