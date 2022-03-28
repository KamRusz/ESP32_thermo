from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.main import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


def date_time():
    return str(datetime.now().strftime("%Y-%m-%d"))


class Temphumi(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True, default=datetime.now)
    temp = db.Column(db.Float)
    humi = db.Column(db.Float)
    day = db.Column(db.String(64), default=date_time)


class Avg_temphumi(db.Model):
    day = db.Column(db.String(64), primary_key=True, default=date_time)
    avg_temp = db.Column(db.Float)
    avg_humi = db.Column(db.Float)


class Targettemp(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True, default=datetime.now)
    target_temp = db.Column(db.Integer)
    by_who = db.Column(db.String(64))


class FailedLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    not_registered_user = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.now)
