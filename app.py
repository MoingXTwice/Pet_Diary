import hashlib

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.petdiary

# 첫 페이지 (로그인 페이지)
@app.route('/')
def home():
    return render_template('index.html')

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

# 회원가입시 아이디 중복 체크


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
