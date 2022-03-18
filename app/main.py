from flask import Flask, render_template
app= Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Kamil'}
    return render_template('index.html', title='Home')

slownik = {"target_temp":"25", "user_override":"1"}