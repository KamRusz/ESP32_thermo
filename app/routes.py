import json
from datetime import date, datetime, timedelta

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm, TempForm
from app.main import app, db
from app.models import Avg_temphumi, FailedLogin, Targettemp, Temphumi, User
from config import Config

temphumi = {"temp": float, "humi": float}


@app.route("/")
@app.route("/index")
def index():
    current_temphumi = (
        db.session.query(Temphumi).order_by(Temphumi.timestamp.desc()).first()
    )
    if not current_temphumi:
        current_temphumi = None
    target_temp = Config.TEMP_TRANS[
        db.session.query(Targettemp)
        .order_by(Targettemp.timestamp.desc())
        .first()
        .target_temp
    ]
    if not target_temp:
        target_temp = None
    data = (
        db.session.query(Avg_temphumi).order_by(Avg_temphumi.day.desc()).limit(10).all()
    )
    labels = [obj.day for obj in data]
    values1 = [obj.avg_temp for obj in data]
    values2 = [obj.avg_humi for obj in data]
    return render_template(
        "index.html",
        title="Home",
        target_temp=target_temp,
        current_temphumi=current_temphumi,
        labels=labels,
        values1=values1,
        values2=values2,
    )


@app.route("/humitemp", methods=["GET", "POST"])
def welcome():
    payload = json.loads(request.data)
    if payload["api_key"] == Config.API_KEY:
        rtemp = float(payload["room_temp"])
        rhumi = float(payload["room_humi"])
        #print("room_temp =", payload["room_temp"])
        temphumi["temp"] = rtemp
        temphumi["humi"] = rhumi
        #print("room_humi =", payload["room_humi"])
        # dodanie do db
        t = Temphumi(temp=rtemp, humi=rhumi)
        db.session.add(t)
        db.session.commit()
        target_temp = (
            db.session.query(Targettemp).order_by(Targettemp.timestamp.desc()).first()
        )
        #print(target_temp.target_temp)
        return {"target_temp": target_temp.target_temp}
    return "zły klucz api"


@app.route("/usertemp", methods=["GET", "POST"])
def welcome2():
    payload = json.loads(request.data)
    if payload["api_key"] == Config.API_KEY:
        print("user_temp =", payload["user_temp"])
        utemp = int(payload["user_temp"])
        t = Targettemp(target_temp=utemp, by_who="ESP")
        db.session.add(t)
        db.session.commit()
        return "user temp overide"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("already logged in")
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = (
            db.session.query(User).filter(User.username == form.username.data).first()
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            u = FailedLogin(not_registered_user=form.username.data)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/settemp", methods=["GET", "POST"])
@login_required
def settemp():
    register = (
        db.session.query(Targettemp)
        .order_by(Targettemp.timestamp.desc())
        .limit(10)
        .all()
    )
    changes = []
    for reg in register:
        changes.append(
            (
                reg.timestamp.strftime("%Y-%m-%d - %H:%M:%S"),
                Config.TEMP_TRANS[reg.target_temp],
                reg.by_who,
            )
        )
    form = TempForm()
    if form.validate_on_submit():
        if not current_user.admin:
            flash("You don't have permission to change this setting")
            return redirect(url_for("settemp"))
        else:
            utemp = int(form.temp.data)
            t = Targettemp(target_temp=utemp, by_who=current_user.username)
            db.session.add(t)
            db.session.commit()
            flash("Target temperature changed")
    return render_template(
        "temp.html",
        title="Set temperature",
        form=form,
        register=register,
        changes=changes,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/adduser", methods=["POST"])
def adduser():
    if Config.ADD_USER_ALLOWED == 'open':
        data = json.loads(request.data)
        if data["add_user_key"] == Config.ADD_USER_KEY:
            username = data["username"]
            password = data["password"]
            admin = int(data["admin"])
            if db.session.query(User).filter(User.username == username).first():
                return "already have this user"
            u = User(username=username, admin=admin)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
        return "user added"
    return "adding users not allowed"


@app.route("/graph")
def home():
    data = (
        db.session.query(Avg_temphumi).order_by(Avg_temphumi.day.desc()).limit(8).all()
    )
    labels = [obj.day for obj in data]
    values1 = [obj.avg_temp for obj in data]
    values2 = [obj.avg_humi for obj in data]

    return render_template(
        "graph.html", labels=labels, values1=values1, values2=values2
    )




'''
@app.route("/test")
def test():
    #data = db.session.query(Temphumi).filter(Temphumi.day < "2022-03-27").first()
    db.session.query(Temphumi).filter(Temphumi.day < "2022-03-27").delete()
    db.session.commit()
    #a = datetime.now() - timedelta(days = 2)
    #print(a.strftime("%Y-%m-%d"))
    #print(data)
    return "ok"
'''