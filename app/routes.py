from flask import Flask, render_template, request

app = Flask(__name__)

from app import app

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/reports')
def reports():
    return render_template('reports.html', title = 'Reports')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/add_equip', methods = ['GET', 'POST'])
def add_equip():
    if request.method == 'POST':
        print("This code will be run when the form is submitted ")
        #animal_name = request.form.get('animal_name')
        #animal_rating = request.form.get('animal_rating')
        return render_template (
            'equip_add.html', 
            #animal_name = animal_name, 
            #animal_rating = animal_rating
        )
    # If we get to this point, then it is a GET request, and we return the view with the form
    return render_template('equip_add.html')

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        print("This code will be run when the form is submitted ")
        #animal_name = request.form.get('animal_name')
        #animal_rating = request.form.get('animal_rating')
        return render_template (
            'user_added.html', 
            #animal_name = animal_name, 
            #animal_rating = animal_rating
        )
    # If we get to this point, then it is a GET request, and we return the view with the form
    return render_template('user_add.html')

@app.route('/add_location', methods = ['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        print("This code will be run when the form is submitted ")
        #animal_name = request.form.get('animal_name')
        #animal_rating = request.form.get('animal_rating')
        return render_template (
            'location_added.html', 
            #animal_name = animal_name, 
            #animal_rating = animal_rating
        )
    # If we get to this point, then it is a GET request, and we return the view with the form
    return render_template('location_add.html')