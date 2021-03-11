from flask import Flask, request, render_template, flash, url_for, redirect
from flask_cors import CORS
from flask_login import LoginManager, login_user, current_user, logout_user
from board_view import board, gallery
from board_control.user_management import User
from db_model.mongodb import conn_board
import os
import datetime

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = os.urandom(24)

app.register_blueprint(board.board_search, url_prefix='/board')
app.register_blueprint(gallery.gallery_search, url_prefix='/gallery')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    collection = conn_board('boardtype')
    result = collection.find({})

    collection = conn_board('boardall')
    sorted_collection = collection.find().sort('hit', -1)
    hit_data = []
    cnt = 0
    for document in sorted_collection:
        cnt += 1
        hit_data.append(document)
        if cnt == 4:
            break

    if current_user.is_authenticated:
        return render_template('index.html', hit_data=hit_data, data=result, userinfo=current_user.user_name)
    else:
        return render_template('index.html', hit_data=hit_data, data=result)

@app.route('/signupa')
def signup():
    return render_template('signup.html')

@app.route('/signupa/post', methods=['POST'])
def signup_post():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']
    user = User.find(user_id, user_pw)
    if user == None:
        new_user = User.create(user_id, user_pw)
        return redirect(url_for('index'))
    else:
        flash('이미 존재하는 사용자입니다.')
        return render_template('signup.html')

@app.route('/userlogin', methods=['POST'])
def user_login():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']
    user = User.find(user_id, user_pw)
    if user == None:
        flash('아이디와 비밀번호를 확인해주세요')
        return redirect(url_for('index'))
    else:
        login_user(user, remember=True, duration=datetime.timedelta(days=1))
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8081", debug=True)