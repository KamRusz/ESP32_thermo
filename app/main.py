from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app= Flask(__name__)
#db = SQLAlchemy(app)

from app import routes