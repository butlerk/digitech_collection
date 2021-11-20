import os
import json
from flask import Flask, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect, secure_filename
from app import app, db
from app.models import Equipment, Location, User, Loan
from app.decorators import admin_required
from app.forms import AddEquipmentForm, AddLocationForm, AddUserForm, EditUserForm, EditEquipmentForm, EditLocationForm, AddLoanForm, EditLoanForm, LoginForm, PhotoForm
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import plotly


# Display the Main page - with bubble visualisation if Admin user. 
@app.route('/')
@login_required
def index():
    query = (
        "SELECT first_name, count(*) loans_per_month, strftime('%m', loan_date) month "
        "FROM loan l "
        "JOIN user u on u.id = l.id "
        "GROUP BY month, u.id "
        "ORDER BY month ASC"
    )

    df = pd.read_sql(query,db.session.bind)
    df = df.sort_values(by="month")
    # Draw the chart and dump it into JSON format
    chart = px.scatter(df, x ="month", y='loans_per_month', color = 'first_name', size="loans_per_month",  labels=
        {"month":"Month", "loans_per_month":"Number of Loans", "first_name":"User *"}, width=900, height=400)
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)
       
    # Return back to the index page to show bubble chart of loans per user per month
    return render_template('index.html', title = 'Loans per month per user', 
        chart_JSON = chart_JSON)

# Display the Login page, check the password for the username entered. 
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

# Logout user and show index page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))



# == LOANS ==
# A route for showing a form and processing form for adding a new loan. 
# Ensures that only avail equipment is able to be chosen
# Admin users can select anyone for loan, General users can only select themselves

@app.route('/add_loan', methods = ['GET', 'POST'])
@login_required
def add_loan():
    form = AddLoanForm()
    date_today = date.today()
    #date_formatted = date_today.strftime("%d/%m/%Y")
    # Create a list of equipment id's on all active loans
    unavail_equip = []
    for loan in Loan.query.filter_by(active = 1).all():
        unavail_equip.append(loan.equip_id)
    # Query the Equipment table to find items that are available (not currently loaned out)
    avail_equip = Equipment.query.filter(Equipment.equip_id.not_in(unavail_equip)).all()
    # Error message if no equipment available
    if len(avail_equip)<1:
        flash(f"No items currently available.")
        return redirect(url_for('view_loan'))
    # Populate equipment dropdown menu with only available items.
    form.equip_id.choices = [(g.equip_id, g.equip_name) for g in avail_equip]

    if current_user.is_admin == True: 
        form.id.choices = [(g.id, g.first_name) for g in User.query.all()]
    else:
        form.id.choices = [(g.id, g.first_name) for g in User.query.filter_by(id = current_user.id).all()]
        
    if form.validate_on_submit():
        loan = Loan()
        form.populate_obj(obj=loan)
        loan.active = 1
        loan.loan_date = date.today()
        db.session.add(loan)
        db.session.commit()
        # Return to the view that shows the list of loans
        return redirect(url_for('view_loan'))

    # Generate the form with the users & equipment in the dropdown box
    return render_template('loan_add.html', form=form, date_today = date_today)

# Queries loan table for loans and archived loans. 
# Displays all loans if admin, but only current user loans if general user
@app.route('/view_loan')
@login_required
def view_loan():
    if current_user.is_admin == False:
        loan = Loan.query.filter_by(id = current_user.id, active = 1).all()
        archievedloan = Loan.query.filter_by(id = current_user.id, active=0).all()
    else: 
        loan = Loan.query.filter_by(active=1).all()
        archievedloan = Loan.query.filter_by(active=0).order_by(Loan.loan_date.desc()).all()
        # Return back to the view that shows the list of loans
    
    query = (
        "SELECT first_name||' '||last_name as user, count(*) as number_of_loans "
        "FROM user u "
        "JOIN loan l on u.id = l.id "
        "GROUP BY user"
    )

    df = pd.read_sql(query,db.session.bind)
    
    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='user', y='number_of_loans',labels=
        {"user": "User","number_of_loans":"Number of Loans"},width=400, height=400)
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

       
    # Return back to the view that shows the list of equipment
    return render_template('loan_view.html', loan=loan, archievedloan=archievedloan, title = 'Number of loans per user', 
        chart_JSON = chart_JSON)



# Sets the selected loan to inactive (archived)
@app.route('/return_loan/<int:id>')
@login_required
def return_loan(id):
    item = Loan.query.get_or_404(id)
    item.active = 0
    db.session.commit()
    flash(f"Successfully returned item {item.loan_id} from the loan list.")
    # Return back to the view that shows the list of loans
    return redirect(url_for('view_loan'))

# A route for processing the deleting of a loan.
#@app.route('/delete_loan/<int:id>')
#@admin_required
#def delete_loan(id):
#    item = Loan.query.get_or_404(id)
#    db.session.delete(item)
#    db.session.commit()
#    flash(f"Successfully deleted loan number {item.loan_id} from the loan list.")
    
    # Return back to the view that shows the list of loans
#    return redirect(url_for('view_loan'))


# == EQUIPMENT ==

# Create an add equipment form - when submitted, create the equipment item and add to database. Return to view with all equipment items.
@app.route('/add_equip', methods = ['GET', 'POST'])
@admin_required
def add_equip():
    
    location = Location.query.all()
    form = AddEquipmentForm(obj=location)
    
    # Retrieve the different locations from the database, for display in a dropdown
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    
    if form.validate_on_submit():
        equipment = Equipment()
        if form.file.data != None:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(app.static_folder, 'images', filename))              
        else:
            filename = "no_image.jpg"
        form.populate_obj(obj=equipment)
        equipment.file = filename
                
        db.session.add(equipment)
        db.session.commit()
        flash(f"Successfully added {equipment.equip_name} as an equipment item.")
        
        # Return back to the view that shows the list of equipment
        return redirect(url_for('view_equip'))

    
    
    
    # Return back to the view that shows equipment form empty
    return render_template('equip_add.html', form=form, location=location)
    

# Display a list of equipment from the database
@app.route('/view_equipment')
@login_required
def view_equip():
    equipment = Equipment.query.all()
    user = current_user
        # Run query to get count of equipment and load into DataFrame
    query = (
        "SELECT equip_name, COUNT(*) as number_of_equipment_borrowed "
        "FROM equipment e "
        "JOIN loan l on e.equip_id = l.equip_id "
        "GROUP BY equip_name"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='equip_name', y='number_of_equipment_borrowed',
        labels = {"equip_name": "Name of Equipment","number_of_equipment_borrowed":"Number of Times borrowed"},
        )
    
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    chart2 = px.pie(df, 
    values = 'number_of_equipment_borrowed', 
    names = "equip_name",
    width=400, 
    height=400, 
    hover_data=['equip_name'], labels={'equip_name':'Equipment:'}
    )
    chart2.update_traces(textposition='inside', textinfo='percent+label')
    chart2.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON2 = json.dumps(chart2, cls=plotly.utils.PlotlyJSONEncoder, indent=4)
    # Return back to the view that shows the list of equipment
    
    return render_template('equip_view.html', equipment=equipment, user=user, title = 'Number of Borrows for each Equipment Item', 
        chart_JSON = chart_JSON, chart_JSON2 = chart_JSON2)

# A route for showing a form and processing form for editing a loan.
@app.route('/edit_equipment/<int:id>', methods = ['GET', 'POST'])
@admin_required
def edit_equipment(id):
    item = Equipment.query.get_or_404(id)
    location = Location.query.all()
    form = EditEquipmentForm(obj=item)
    # Retrieve the different locations from the database, for display in a dropdown
    form.location_id.choices = [(g.location_id, g.location_name) for g in location]
    form.file = item.file
     # When the form is submitted, the form is processed and save to the equipment database
    if form.validate_on_submit():
        form.populate_obj(obj=item)
        form.file = item.file
        db.session.commit()
        flash(f"Successfully saved {item.equip_name} equipment item.")
        
        # Return back to the view that shows the list of equipment
        return redirect(url_for('view_equip'))
    
    # Return back to the view that add equipment fields empty
    return render_template('equip_edit.html', form=form, location=location)

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
    if form.validate_on_submit():
        # When the form is submitted, the form is processed and save to the user database        
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
    if current_user.is_admin == False:
        users = User.query.filter_by(id = current_user.id).all()
    else: 
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
    if form.validate_on_submit():
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
        flash(f"Can not delete this location as there is equipment at this location.")
    else:
        location = Location.query.get_or_404(id)
        db.session.delete(location)
        db.session.commit()
        flash(f"Successfully deleted the location {location.location_name}.")

    # Return back to the view that shows the list of locations    
    return redirect(url_for('view_location'))

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


#renders the Chart list page
@app.route('/view_charts')
@login_required
def view_charts():
    return render_template('chart_list.html', title = 'List of Charts')

#create a chart of borrows/loans per year
@app.route('/borrows_per_year')
@login_required
def borrows_per_year_chart():
    query = (
        "SELECT substr(loan_date,0,5) year,count(*) as num_borrows_per_year " 
        "FROM loan l " 
        "GROUP BY substr(loan_date,0,5)"
    )
    df = pd.read_sql(query, db.session.bind)
  
    # Draw the chart and dump it into JSON format
    chart = px.line(df, x ='year', y='num_borrows_per_year')
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Return back to the view that displays on the charts page 
    return render_template('chart_page.html', title = 'Total Borrows per year', 
        chart_JSON = chart_JSON)

#create chart of loans per user
@app.route('/loans_by_user')
@login_required
def loans_by_user_chart():
    query = (
        "SELECT first_name||' '||last_name as user, count(*) as number_of_loans "
        "FROM user u "
        "JOIN loan l on u.id = l.id "
        "GROUP BY first_name||' '||last_name"
    )

    df = pd.read_sql(query,db.session.bind)
 
    
    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='user', y='number_of_loans',labels=
        {"user": "User","number_of_loans":"Number of Loans"},width=400, height=400)
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

       
    # Return back to the view that displays on the charts page
    return render_template('chart_page.html', title = 'Number of loans per user', 
        chart_JSON = chart_JSON)

#create a chart which displays loans per month
@app.route('/loans_by_month')
@login_required
def loans_by_month_chart():
    query = (
        "SELECT strftime('%Y', loan_date) year, count(*) loans_per_month, strftime('%m', loan_date) month "
        "FROM loan "
        "GROUP BY month "
        "ORDER BY year, month ASC"
    )

    df = pd.read_sql(query,db.session.bind)
    df = df.sort_values(by="month")
    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='month', y='loans_per_month', color='month', labels=
        {"month": "Month","loans_per_month":"Number of Loans", "year":"Year"},width=600, height=400)
    
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

       
    # Return back to the view that shows the chart page
    return render_template('chart_page.html', title = 'Number of loans per month', 
        chart_JSON = chart_JSON)

#create a chart to show the number of loans per month by user
@app.route('/loans_by_month_by_user')
@login_required
def loans_by_month_by_user_chart():
    query = (
        "SELECT first_name, count(*) loans_per_month, strftime('%m', loan_date) month "
        "FROM loan l "
        "JOIN user u on u.id = l.id "
        "GROUP BY month, u.id "
        "ORDER BY month ASC"
    )

    df = pd.read_sql(query,db.session.bind)
    df = df.sort_values(by="month")
    # Draw the chart and dump it into JSON format
    chart = px.line(df, x ='month', y='loans_per_month', color = 'first_name', symbol = "first_name",  labels=
        {"month": "Month","loans_per_month":"Number of Loans", "first_name":"User - click on names to change view"},width=900, height=400)
    chart.update_layout({
        'plot_bgcolor':'rgba(0, 0, 0, 0)',
        'paper_bgcolor':'rgba(0, 0, 0, 0)'})
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

       
    # Return back to the view that displays the charts
    return render_template('chart_page.html', title = 'Number of loans per month per user', 
        chart_JSON = chart_JSON)


