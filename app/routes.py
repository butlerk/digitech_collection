from flask import render_template

from app import app

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')


@app.route('/helloworld')
def helloworld():
    return render_template('helloworld.html', title = 'HelloWorld')

