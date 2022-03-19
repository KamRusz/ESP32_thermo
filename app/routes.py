from flask import render_template, request, redirect, flash, url_for
import datetime
from app.main import app
from app.forms import LoginForm
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kamil'}
    return render_template('index.html', title='Home')

slownik = {"target_temp":"25", "user_override":"1"}

@app.route('/hello', methods=['GET','POST'])
def welcome():   
    payload = json.loads(request.data)
    print("api =",payload["api_key"])
    print("room_temp =",payload["room_temp"])
    print("room_humi =",payload["room_humi"])
    return slownik
    #print(request.args["temp"],request.args["humi"])
    #if api_key == "123456789":
    #    return slownik
    #else:
    #    return "zonk"

@app.route('/hello2', methods=['GET','POST'])
def welcome2():   
    payload = json.loads(request.data)
    print("user_temp =",payload["user_temp"])
    return "user temp overide"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)