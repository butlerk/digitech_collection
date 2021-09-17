from flask import render_template

from app import app

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/reports')
def reports():
    return render_template('reports.html', title = 'Reports')

@app.route('/locations')
def locations():
    return render_template('locations.html', title = 'Locations')

@app.route('/equipment')
def equipment():
    return render_template('equipment.html', title = 'Equipment')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/users')
def users():
    return render_template('users.html', title = 'Users')

@app.route('/new_user')
def new_user():
    return render_template('new_user.html', title = 'New User')

@app.route('/add_equip_success')
def add_equip_success():
    return render_template('add_equip_success.html', title = 'Add Equipment Success')

@app.route('/add_user_success')
def add_user_success():
    return render_template('add_user_success.html', title = 'Add User Success')

@app.route('/add_location_success')
def add_location_success():
    return render_template('add_location_success.html', title = 'Add Location Success')



