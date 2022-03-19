from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
import os

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#db = SQLAlchemy(app)
alembic = Alembic()
alembic.init_app(app)


from app import routes, models