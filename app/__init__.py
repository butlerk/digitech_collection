
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime, date
from numpy import genfromtxt
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

# Set up login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models

# Load dummy data from csv file and convert to date
def Load_Data(file_name):
    str2date = lambda x: datetime.strptime(x, '%Y-%m-%d')     
    data = genfromtxt(file_name, dtype=(datetime, int, int, int), delimiter=',', skip_header=1, converters = {0:str2date}, encoding = 'utf-8')
    return data.tolist()

# Initialise the Database
@app.cli.command('init-db')
def init_db():

    # Create the database for the app from scratch
    db.drop_all()
    db.create_all()

    # Create location item records to populate db
    library = models.Location(location_name = 'Library')
    db.session.add(library)
    
    storeroom = models.Location(location_name  = 'Storeroom')
    db.session.add(storeroom)
    
    # Create equipment item records to populate db
    microbit = models.Equipment (
        equip_name  = 'Microbit',
        location = library,
        purchase_price = 29.40,
        equip_details = "A set of 20 Micro:bit V2 with USB cables and battery packs",
        purchase_date= date.today(),
        file = 'microbit.png',      
    )
    db.session.add(microbit)

    beebot = models.Equipment (
        equip_name  = 'Beebot',
        location = storeroom,
        purchase_price = 5.40,
        equip_details = "A set of 15 Beebots with chargers",
        purchase_date = date(2021,1,3),
        file = 'beebot.jpeg',
    )
    db.session.add(beebot)

    makeymakey = models.Equipment (
        equip_name  = 'Makey-Makey',
        location = storeroom,
        purchase_price = 10.40,
        equip_details = "A set of 10 Makey-Makeys",
        purchase_date= date(2020,10,3),
        file = 'makeymakey.jfif',
    )
    db.session.add(makeymakey)

    # Create user items records to populate db

    person1 = models.User (
        first_name  = 'Kelly',
        last_name = 'Butler',
        email_username = 'kelly@email.com',
        is_admin=True
    )
    person1.password = os.environ.get('KELLY_PASSWORD')
    db.session.add(person1)
    
    person2 = models.User (
        first_name  = 'Kirsty',
        last_name = 'Watts',
        email_username = 'kirsty@email.com',
        is_admin=False
    )
    person2.password = os.environ.get('KIRSTY_PASSWORD')
    db.session.add(person2)

    person3 = models.User (
        first_name  = 'Joe',
        last_name = 'Blogs',
        email_username = 'joe@email.com',
        is_admin=False
    )
    person3.password = os.environ.get('JOE_PASSWORD')
    db.session.add(person3)

     # Create loan item records to populate db
    loan1 = models.Loan (
        loan_date = date(2020,2,10),
        id = 1,
        equip_id = 1,
        active = True
    )
    db.session.add(loan1)

    loan2 = models.Loan (
        loan_date = date(2019,5,12),
        id = 2,
        equip_id = 2,
        active = False
    )
    db.session.add(loan2)
    
    # Import dummy data from csv file
    file_name = "archive.csv"
    data = Load_Data(file_name)
    for i in data:
        loan = models.Loan(**{
            'loan_date': i[0],
            'id' : i[1],
            'equip_id' : i[2],
            'active' : i[3],
        })
        db.session.add(loan) #Add all the records
        # Save the created records to the database file
        db.session.commit()
