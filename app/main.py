from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_login import LoginManager
import os
from config import Config

app= Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
alembic = Alembic()
alembic.init_app(app)
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models