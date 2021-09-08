from flask import render_template

from app import app

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/loans')
def loans():
    return render_template('loans.html', title = 'Loans')

@app.route('/reports')
def reports():
    return render_template('reports.html', title = 'Reports')

@app.route('/locations')
def locations():
    return render_template('locations.html', title = 'Locations')

@app.route('/users')
def users():
    return render_template('users.html', title = 'Users')

