import os
from flask import Flask, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import redirect, secure_filename
#from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Equipment, Location, User, Loan
from app.decorators import admin_required
from app.forms import AddEquipmentForm, AddLocationForm, AddUserForm, EditUserForm, EditEquipmentForm, EditLocationForm, AddLoanForm, EditLoanForm, LoginForm, PhotoForm
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

UPLOAD_FOLDER = 'app/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
@login_required
def index():
     # Return back to the home page
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user based off the name that has been entered in form
        user = User.query.filter_by(email_username=form.email_username.data).first()
        # Check if the user actually exists in the database
        if user is not None:
            # Check if the correct password has been entered and login, if so
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('index'))
        flash('Invalid username or password')

    # If there is a GET request, or there are errors in the form, return the view with the form
    return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))





# == LOANS ==

# A route for showing a form and processing form for adding a new loan.
@app.route('/add_loan', methods = ['GET', 'POST'])
@login_required
def add_loan():
    form = AddLoanForm()

    # Retrieve the users from the database, for display in a dropdown
    form.id.choices = [(g.id, g.first_name) for g in User.query.all()]

    # Retrieve the equipment from the database, for display in a dropdown
    form.equip_id.choices = [(g.equip_id, g.equip_name) for g in Equipment.query.all()]
    form.loan_date = date.today()

    # When the form is submitted, the form is processed and save to the loans database
    if form.validate_on_submit():
        loan = Loan()
        loan.loan_date = datetime.now()
        form.populate_obj(obj=loan)
        db.session.add(loan)
        db.session.commit()

        # Return to the view that shows the list of loans
        return redirect(url_for('view_loan'))

    # Generate the form with the users & equipment in the dropdown box
    return render_template('loan_add.html', form=form)

# A route for showing a query of all loans.
@app.route('/view_loan')
@login_required
def view_loan():
    loan = Loan.query.all()
    
    # Return back to the view that shows the list of loans
    return render_template('loan_view.html', loan=loan)

# A route for processing the deleting of a loan.
@app.route('/delete_loan/<int:id>')
@admin_required
def delete_loan(id):
    item = Loan.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash(f"Successfully deleted loan number {item.loan_id} from the loan list.")
    
    # Return back to the view that shows the list of loans
    return redirect(url_for('view_loan'))

# A route for showing and processing form for editing a loan.
@app.route('/edit_loan/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_loan(id):
    item = Loan.query.get_or_404(id)
    form = EditLoanForm(obj=item)
    form.id.choices = [(user.id, user.first_name) for user in User.query.all()]
    form.equip_id.choices = [(equip.equip_id, equip.equip_name) for equip in Equipment.query.all()]
    
    # When the form is submitted, the form is processed and saved to the loans table.
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f"Successfully saved loan number {item.loan_id}.")
        
        # Return back to the view that shows the list of loans
        return redirect(url_for('view_loan'))
    
    # Return back to the view that shows the loan form empty
    return render_template('loan_add.html', form=form)

# == EQUIPMENT ==

# Create an add equipment form - when submitted, create the equipment item and add to database. Return to view with all equipment items.
@app.route('/add_equip', methods = ['GET', 'POST'])
@admin_required
def add_equip():
    form = AddEquipmentForm()
    if request.method == 'POST':
        equipment = Equipment()
        form.populate_obj(obj=equipment)
        db.session.add(equipment)
        db.session.commit()
        flash(f"Successfully added {equipment.equip_name} as an equipment item.")
        
        # Return back to the view that shows the list of equipment
        return redirect(url_for('view_equip'))
       
    # Generate the form with the locations in the dropdown box
    location = Location.query.all()
    form = AddEquipmentForm(obj=location)
    
    # Retrieve the different locations from the database, for display in a dropdown
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    
    # Return back to the view that shows equipment form empty
    return render_template('equip_add.html', form=form, location=location)

# Display a list of equipment from the database
@app.route('/view_equipment')
@login_required
def view_equip():
    equipment = Equipment.query.all()
    
    # Return back to the view that shows the list of equipment
    return render_template('equip_view.html', equipment=equipment)

# A route for showing a form and processing form for editing a loan.
@app.route('/edit_equipment/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_equipment(id):
    item = Equipment.query.get_or_404(id)
    location = Location.query.all()
    form = EditEquipmentForm(obj=item)
    # Retrieve the different locations from the database, for display in a dropdown
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    
    # When the form is submitted, the form is processed and save to the equipment database
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash(f"Successfully saved {item.equip_name} equipment item.")
        
        # Return back to the view that shows the list of equipment
        return redirect(url_for('view_equip'))
    
    # Return back to the view that add equipment fields empty
    return render_template('equip_add.html', form=form, location=location)

# Delete a specific equipment item - retrieving, deleting and committing changes to the database. Returns to list of equipment
@app.route('/delete_equipment/<int:id>')
@admin_required
def delete_equipment(id):
    item = Equipment.query.get_or_404(id)
    
    # When delete button is pressed, equipment database queried for loans with equipment_id in
    # them and displays error message
    if len(Loan.query.filter_by(equip_id = id).all())>0:
        flash(f"Cannot delete this item as there are loans associated with it")
    else:
        db.session.delete(item)
        db.session.commit()
        flash(f"Successfully deleted {item.equip_name} from the equipment list.")
    
    # Return back to the view that shows the list of equipment
    return redirect(url_for('view_equip'))

# == USERS ==

# Create an add user form - when submitted, create the user and add to database. Return to view with all locations.
@app.route('/add_user', methods = ['GET', 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if request.method == 'POST':
        
        # When the form is submitted, the form is processed and save to the user database
        if form.validate_on_submit:
            user = User()
            form.populate_obj(obj=user)
            db.session.add(user)
            db.session.commit()
            flash(f"Successfully added {user.first_name} {user.last_name} as user.")
            
            # Return back to the view that shows the list of users
            return redirect(url_for('view_user'))
    
    # Return back to the view of empty user fields
    return render_template('user_add.html', form=form)

# A route for querying and displaying all users.
@app.route('/view_user')
@login_required
def view_user():
    users = User.query.all()
    
    # Return back to the view that shows the list of users
    return render_template('user_view.html', users=users)


# A route for showing a form and processing form for adding a new loan.
@app.route('/edit_user/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    
    # When the form is submitted, the form is processed and save to the user database
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash(f"Successfully saved {user.first_name} {user.last_name}.")
        
        # Return back to the view that shows the list of users
        return redirect(url_for('view_user'))

    # Returns the queried user information in the user form for editing
    return render_template('user_edit.html', form = form)

# Delete a specific user - retrieving, deleting and committing changes to the database. Returns to list of locations
@app.route('/delete_user/<int:id>')
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    # When delete button is pressed, user database queried for loans with id in
    # them and displays error message
    if len(Loan.query.filter_by(id = id).all()) > 0:
        flash(f"Can not delete {user.first_name} {user.last_name} as they have loans associated with them.")
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f"Successfully deleted {user.first_name} {user.last_name}.")
    
    # Return back to the view that shows the list of users
    return redirect(url_for('view_user'))
    


# == LOCATIONS ==

# Create an add a location form - when submitted, create the location and add to database. Return to view with all locations.
@app.route('/add_location', methods = ['GET', 'POST'])
@admin_required
def add_location():
    form=AddLocationForm()
    location = Location.query.all()
    if request.method == 'POST':
        location = Location()
        form.populate_obj(obj=location)
        db.session.add(location)
        db.session.commit()
        flash(f"Successfully added {location.location_name} as a location.")
        
        # Return back to the view that shows the list of locations
        return redirect(url_for ("view_location"))

    # Return back to the view that shows the form to add a location
    return render_template('location_add.html', form=form)

# View all locations in the database
@app.route('/view_location')
@login_required
def view_location():
    location = Location.query.all()

    # Return back to the view that shows the list of locations
    return render_template('location_view.html', location=location)

# Edit a location in the database, retrieving the location record if it exists, creating a form and populating the form with existing data.
@app.route('/edit_location/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_location(id):
    location = Location.query.get_or_404(id)
    form = EditLocationForm(obj=location)
    
    # When the form is submitted, the form is processed and save to the locations database
    if form.validate_on_submit():
        form.populate_obj(location)
        db.session.commit()
        flash(f"Successfully saved {location.location_name} as a location.")

        # Return back to the view that shows the list of locations
        return redirect(url_for('view_location'))

    # Return back to the view that shows the location item in a form for editing    
    return render_template('location_edit.html', form = form)

# Delete a specific location - retrieving, deleting and committing changes to the database. Returns to list of locations
@app.route('/delete_location/<int:id>')
@admin_required
def delete_location(id):    
    equipment_at_location = Equipment.query.filter_by(location_id = id)
    
    # When delete button is pressed, equipment database queried for locations with equipment_id in
    # them and displays error message
    if len(equipment_at_location.all()) > 0:
        flash(f"Can not delete this location as there are equipment at this location")
    else:
        location = Location.query.get_or_404(id)
        db.session.delete(location)
        db.session.commit()
        flash(f"Successfully deleted the location {location.location_name}.")

    # Return back to the view that shows the list of locations    
    return redirect(url_for('view_location'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.static_folder, 'images', filename
        ))
        flash(f"Successfully uploaded the photo.")
        return redirect(url_for('index'))
    return render_template('upload_photo.html', form=form)








 #   if form.validate_on_submit():
 #       if request.method == 'POST':
 #           if 'file' not in request.files:
 #               flash('No file part')
 #               return redirect(url_for('index'))
 ##           file = request.files['file']
 #           if file.filename == '':
 #               flash('No selected file')
 #               return redirect(url_for('index'))
 #           if file and allowed_file(file.filename):
 #               filename = secure_filename(file.filename)
 #               file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 #               flash('File successfully uploaded')
 #               return redirect(url_for('index'))
 #   return


            



#    

    
        # check if the post request has the file part
        
            
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        
