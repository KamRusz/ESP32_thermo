from datetime import date
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user ,login_required
from werkzeug.urls import url_parse
from app.main import app, db
from app.forms import LoginForm, TempForm
from app.models import FailedLogin, Temphumi, User, Avg_temphumi, Targettemp
from config import Config
import json

temphumi = {'temp': 25, "humi": 45}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

slownik = {"target_temp":"25"}

@app.route('/humitemp', methods=['GET','POST'])
def welcome():   
    payload = json.loads(request.data)
    #print(Config.API_KEY)
    #print("api =",payload["api_key"])
    #print(payload["api_key"] == Config.API_KEY)
    if payload["api_key"] == Config.API_KEY:
        rtemp = int(payload["room_temp"])
        rhumi = int(payload["room_humi"])
        print("room_temp =",payload["room_temp"])
        temphumi["temp"] = rtemp
        temphumi["humi"] = rhumi
        print("room_humi =",payload["room_humi"])
        #dodanie do db
        t = Temphumi(temp = rtemp , humi = rhumi)
        db.session.add(t)
        db.session.commit()
        #target_temp = db.session.query(Targettemp).order_by(Targettemp.timestamp.desc()).first()
        #return {"target_temp":target_temp}
        return slownik
    return "zły klucz api"

@app.route('/usertemp', methods=['GET','POST'])
def welcome2():   
    payload = json.loads(request.data)
    if payload["api_key"] == Config.API_KEY:
        print("user_temp =",payload["user_temp"])
        utemp = int(payload["user_temp"])
        t = Targettemp(target_temp = utemp , by_who="ESP")
        db.session.add(t)
        db.session.commit()
        return "user temp overide"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("already logged in")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            u = FailedLogin(not_registered_user =form.username.data)
            db.session.add(u)
            db.session.commit()
            not_registered_user = db.Column(db.String(64))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/settemp', methods=['GET', 'POST'])
@login_required
def settemp():
    form = TempForm()
    print("user = ",current_user.username)
    if form.validate_on_submit():
        if not current_user.admin:
            flash('Not admin')
            return redirect(url_for('settemp'))
        else:
            utemp = int(form.temp.data)
            print(utemp)
            t = Targettemp(target_temp = utemp , by_who=current_user.username)
            db.session.add(t)
            db.session.commit()
            flash("Target temperature changed")
    return render_template('temp.html', title='Set temperature', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/adduser', methods=['POST'])
def adduser():
    data = json.loads(request.data)
    if data["add_user_key"] == Config.ADD_USER_KEY:
        username = data['username']
        password = data['password']
        admin = int(data['admin'])
        print(username, password, admin)
        u = User(username = username, admin = admin)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
    return "user added"