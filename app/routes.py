from flask import render_template, request
import datetime
from app.main import app
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kamil'}
    return render_template('index.html', title='Home')

slownik = {"target_temp":"25", "user_override":"1"}