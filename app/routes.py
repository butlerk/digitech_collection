from flask import Flask, render_template, request
#from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Equipment

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
        equip_name = request.form.get('equip_name')
        location = request.form.get('location')
        equipment_quantity = request.form.get('equipment_quantity')
        available = request.form.get('available_for_loan')
        filename = request.form.get('file')

        return render_template (
            'equip_added.html', 
            equip_name = equip_name, 
            location = location, 
            equipment_quantity = equipment_quantity,
            available_for_loan = available,
            filename = filename 
           
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