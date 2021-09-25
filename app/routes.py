from flask import Flask, render_template, request
#from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Equipment

@app.route('/')

@app.route('/index')
def index():
    
    # Retrieves all of the records in the fruit table
    return render_template('index.html')

@app.route('/reports')
def reports():
    return render_template('reports.html', title = 'Reports')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/add_equip', methods = ['GET', 'POST'])

def add_equip():
    equipment = Equipment.query.all()
    if request.method == 'POST':
        print("This code will be run when the form is submitted ")
        equipment = Equipment(
            equip_name = request.form.get('equip_name'),
            location_id = request.form.get('location_id'),
            equip_quantity = request.form.get('equip_quantity'),
            date_entered = "date34",
            equip_image = request.form.get('equip_image')
         )
        db.session.add(equipment)
        db.session.commit()
        
        # Returns the view with a message that the student has been added
        return render_template('equip_added.html', equipment=equipment)

    # When there is a GET request, the view with the form is returned
    return render_template('equip_add.html')

@app.route('/equip_view')
def view_equip():
    equipment = Equipment.query.all()
    return render_template('equip_view.html', equipment=equipment)

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