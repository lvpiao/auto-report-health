# encoding:utf-8

import main
import db
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    # print(request.form)
    # return "你的账号已成功开启自动打卡功能，如需要取消自动打卡请联系：QQ 2033465789"
    print("login",request.form['appId'], request.form['password'])
    db.insert((request.form['appId'], request.form['password'], None))
    return  render_template('success.html')


@app.route('/cancel_item', methods=['POST'])
def cancel_item():
    # print(request.form)
    # return "你的账号已成功开启自动打卡功能，如需要取消自动打卡请联系：QQ 2033465789"
    print("cancel_item",(request.form['appId'], request.form['password']))
    db.delete((request.form['appId'], request.form['password']))
    print(db.alluser())
    return  render_template('cancel_success.html')

@app.route('/cancel', methods=['GET'])
def cancel():
    return  render_template('cancel.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
