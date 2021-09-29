from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
#from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Equipment, Location, User
from app.forms import AddEquipmentForm, AddLocationForm, AddUserForm, EditUserForm, EditEquipmentForm
from sqlalchemy.orm import sessionmaker

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/reports')
def reports():
    return render_template('reports.html', title = 'Reports')

@app.route('/login')
def login():
    return render_template('login.html', title = 'Login')

@app.route('/add_equip', methods = ['GET', 'POST'])
def add_equip():
    form = AddEquipmentForm()
    if request.method == 'POST':
        #if form.validate_on_submit():
            equipment = Equipment()
            form.populate_obj(obj=equipment)
            db.session.add(equipment)
            db.session.commit()
            return redirect(url_for('view_equip'))
    # When there is a GET request, the view with the form is returned
    location = Location.query.all()
    form = AddEquipmentForm(obj=location)
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    return render_template('equip_add.html', form=form, location=location)

@app.route('/view_equipment')
def view_equip():
    equipment = Equipment.query.all()
    return render_template('equip_view.html', equipment=equipment)

@app.route('/edit_equipment/<int:id>', methods = ['GET', 'POST'])
def edit_equipment(id):
    # Retrieves the user record for the given id, if it exists
    equipment = Equipment.query.get_or_404(id)
    
    # Creates a form for editing the user record, putting in the fruit record's details
    form = EditEquipmentForm(obj=equipment)

    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid

        # The inputs are used to change the fruit's attributes
        form.populate_obj(equipment)
        # The changes to the fruit are saved in the database
        db.session.commit()
        # Returns back to the view that displays the list of fruits
        
        return redirect(url_for('view_equipment'))

    # When there is a GET request or when the inputs are invalid, the view with the form is returned
    location = Location.query.all()
    form = AddEquipmentForm(obj=location)
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    return render_template('equip_add.html', form=form, location=location)

    
@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            user = User()
            form.populate_obj(obj=user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('view_user'))
    return render_template('user_add.html', form=form)

@app.route('/view_user')
def view_user():
    users = User.query.all()
    return render_template('user_view.html', users=users)

@app.route('/edit_user/<int:id>', methods = ['GET', 'POST'])
def edit_user(id):
    # Retrieves the user record for the given id, if it exists
    user = User.query.get_or_404(id)
    
    # Creates a form for editing the user record, putting in the fruit record's details
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        # The form has been submitted and the inputs are valid

        # The inputs are used to change the fruit's attributes
        form.populate_obj(user)
        # The changes to the fruit are saved in the database
        db.session.commit()
        # Returns back to the view that displays the list of fruits
        return redirect(url_for('view_user'))

    # When there is a GET request or when the inputs are invalid, the view with the form is returned
    return render_template('user_edit.html', form = form)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    # Retrieves the user record for the given id
    user = User.query.get_or_404(id)
    # The user record is deleted
    db.session.delete(user)
    # The change (the deletion) are saved in the database file
    db.session.commit()
    # Returns the view that displays the list of users
    return redirect(url_for('view_user'))


@app.route('/add_location', methods = ['GET', 'POST'])
def add_location():
    form=AddLocationForm()
    location = Location.query.all()
    if request.method == 'POST':
        print("This code will be run when the form is submitted ")
        location = Location()
        form.populate_obj(obj=location)

        db.session.add(location)
        db.session.commit()
        return redirect(url_for ("view_location"))
    # If we get to this point, then it is a GET request, and we return the view with the form
    return render_template('location_add.html', form=form)

@app.route('/view_location')
def view_location():
    location = Location.query.all()
    return render_template('location_view.html', location=location)