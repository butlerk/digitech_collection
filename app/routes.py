from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
#from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Equipment, Location, User, Loan
from app.forms import AddEquipmentForm, AddLocationForm, AddUserForm, EditUserForm, EditEquipmentForm, EditLocationForm, AddLoanForm, EditLoanForm
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

# == LOANS ==

@app.route('/add_loan', methods = ['GET', 'POST'])
def add_loan():
    form = AddLoanForm()
    form.user_id.choices = [(g.user_id, g.first_name) for g in User.query.all()]
    form.equip_id.choices = [(g.equip_id, g.equip_name) for g in Equipment.query.all()]
    form.loan_date = datetime.now()
    if form.validate_on_submit():
        loan = Loan()
        form.populate_obj(obj=loan)
        db.session.add(loan)
        db.session.commit()
        return redirect(url_for('view_loan'))
    # Generate the form with the users & equipment in the dropdown box
    return render_template('loan_add.html', form=form)

@app.route('/view_loan')
def view_loan():
    loan = Loan.query.all()
    return render_template('loan_view.html', loan=loan)

@app.route('/delete_loan/<int:id>')
def delete_loan(id):
    item = Loan.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f"Successfully deleted loan number {item.loan_id} from the loan list.")
    return redirect(url_for('view_loan'))


@app.route('/edit_loan/<int:id>', methods = ['GET', 'POST'])
def edit_loan(id):
    item = Loan.query.get_or_404(id)
    form = EditLoanForm(obj=item)
    form.user_id.choices = [(user.user_id, user.first_name) for user in User.query.all()]
    form.equip_id.choices = [(equip.equip_id, equip.equip_name) for equip in Equipment.query.all()]
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f"Successfully saved {item.equip_id} equipment item.")
        return redirect(url_for('view_loan'))
    return render_template('loan_add.html', form=form)


# == EQUIPMENT ==

# Create an add equipment form - when submitted, create the equipment item and add to database. Return to view with all equipment items.
@app.route('/add_equip', methods = ['GET', 'POST'])
def add_equip():
    form = AddEquipmentForm()
    if request.method == 'POST':
        equipment = Equipment()
        form.populate_obj(obj=equipment)
        db.session.add(equipment)
        db.session.commit()
        flash(f"Successfully added {equipment.equip_name} as an equipment item.")
        return redirect(url_for('view_equip'))
    # Generate the form with the locations in the dropdown box
    location = Location.query.all()
    form = AddEquipmentForm(obj=location)
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    return render_template('equip_add.html', form=form, location=location)



# Display a list of equipment from the database
@app.route('/view_equipment')
def view_equip():
    equipment = Equipment.query.all()
    return render_template('equip_view.html', equipment=equipment)



# Edit a specific equipment item in the database, retrieving the equipment record if it exists, creating a form and populating the form with existing data.
# If submit form is pressed and form is valid, the inputs are used to change the equipment attribues and changes are saved in the database
# If GET request, or inputs invalid, the view with the form is returned
# Return to list of equipment
@app.route('/edit_equipment/<int:id>', methods = ['GET', 'POST'])
def edit_equipment(id):
    item = Equipment.query.get_or_404(id)
    location = Location.query.all()
    form = EditEquipmentForm(obj=item)
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f"Successfully saved {item.equip_name} equipment item.")
        return redirect(url_for('view_equip'))
    return render_template('equip_add.html', form=form, location=location)

# Delete a specific equipment item - retrieving, deleting and committing changes to the database. Returns to list of equipment
@app.route('/delete_equipment/<int:id>')
def delete_equipment(id):
    item = Equipment.query.get_or_404(id)
    if len(Loan.query.filter_by(equip_id = id).all())>0:
        flash(f"Cannot delete this item as there are loans associated with it")
    else:
        db.session.delete(item)
        db.session.commit()
        flash(f"Successfully deleted {item.equip_name} from the equipment list.")
    return redirect(url_for('view_equip'))

# == USERS ==

# Create an add user form - when submitted, create the user and add to database. Return to view with all locations.
@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            user = User()
            form.populate_obj(obj=user)
            db.session.add(user)
            db.session.commit()
            flash(f"Successfully added {user.first_name} {user.last_name} as a user.")
            return redirect(url_for('view_user'))
    return render_template('user_add.html', form=form)

# View a user & write to database
@app.route('/view_user')
def view_user():
    users = User.query.all()
    return render_template('user_view.html', users=users)

# Edit a specific user in the database, retrieving the user record if it exists, creating a form and populating the form with existing data.
# If submit form is pressed and form is valid, the inputs are used to change the users's attribues and changes are saved in the database
# If GET request, or inputs invalid, the view with the form is returned
# Return to list of users
@app.route('/edit_user/<int:id>', methods = ['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash(f"Successfully saved {user.first_name} {user.last_name}.")
        return redirect(url_for('view_user'))

    return render_template('user_edit.html', form = form)

# Delete a specific user - retrieving, deleting and committing changes to the database. Returns to list of locations
@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    if len(Loan.query.filter_by(user_id = id).all()) > 0:
        flash(f"Can not delete {user.first_name} {user.last_name} as they have loans associated with them.")
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f"Successfully deleted {user.first_name} {user.last_name}.")
    return redirect(url_for('view_user'))
    


# == LOCATIONS ==

# Create an add a location form - when submitted, create the location and add to database. Return to view with all locations.
@app.route('/add_location', methods = ['GET', 'POST'])
def add_location():
    form=AddLocationForm()
    location = Location.query.all()
    if request.method == 'POST':
        location = Location()
        form.populate_obj(obj=location)
        db.session.add(location)
        db.session.commit()
        flash(f"Successfully added {location.location_name} as a location.")
        return redirect(url_for ("view_location"))
    return render_template('location_add.html', form=form)

# View all locations in the database
@app.route('/view_location')
def view_location():
    location = Location.query.all()
    return render_template('location_view.html', location=location)

# Edit a specific location in the database, retrieving the location record if it exists, creating a form and populating the form with existing data.
# If submit form is pressed and form is valid, the inputs are used to change the location's attribues and changes are saved in the database
# If GET request, or inputs invalid, the view with the form is returned
# Return to list of locations
@app.route('/edit_location/<int:id>', methods = ['GET', 'POST'])
def edit_location(id):
    location = Location.query.get_or_404(id)
    form = EditLocationForm(obj=location)
    if form.validate_on_submit():
        form.populate_obj(location)
        db.session.commit()
        flash(f"Successfully saved {location.location_name} as a location.")
        return redirect(url_for('view_location'))
    return render_template('location_edit.html', form = form)

# Delete a specific location - retrieving, deleting and committing changes to the database. Returns to list of locations
@app.route('/delete_location/<int:id>')
def delete_location(id):    
    equipment_at_location = Equipment.query.filter_by(location_id = id)
    if len(equipment_at_location.all()) > 0:
        flash(f"Can not delete this location as there are equipment at this location")
    else:
        location = Location.query.get_or_404(id)
        db.session.delete(location)
        db.session.commit()
        flash(f"Successfully deleted the location {location.location_name}.")
    return redirect(url_for('view_location'))

    
## Not currently used
# @app.route('/reports')
# def reports():
#    return render_template('reports.html', title = 'Reports')

# @app.route('/login')
# def login():
#    return render_template('login.html', title = 'Login')