
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'example-secret' 


db = SQLAlchemy(app)

# Set up login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models

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
        equip_quantity = 1,
        date_entered = '2021-04-04',
        file = 'image.jpg',
        
    )
    db.session.add(microbit)

    beebot = models.Equipment (
        equip_name  = 'Beebot',
        location = storeroom,
        purchase_price = 5.40,
        equip_quantity = 10,
        date_entered = '2021-05-01',
        file = 'image1.jpg',
        
    )
    db.session.add(beebot)

    # Create user item records to populate db
    person1 = models.User (
        first_name  = 'Kelly',
        last_name = 'Butler',
        email_username = 'kelly@email.com',
        #password = 'hello',
        is_admin=True
    )
    person1.password = 'hello'
    db.session.add(person1)
    
    person2 = models.User (
        first_name  = 'Kirsty',
        last_name = 'Watts',
        email_username = 'kirsty@email.com',
        #password = 'goodbye',
        is_admin=False
    )
    person2.password = 'goodbye'
    db.session.add(person2)

     # Create loan item records to populate db
    loan1 = models.Loan (
        loan_date = datetime.now(),
        id = 1,
        equip_id = 1
    )
    db.session.add(loan1)
        

    # Save the created records to the database file
    db.session.commit()
