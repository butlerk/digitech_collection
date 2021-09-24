from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'

app.config['SECRET_KEY'] = 'example-secret' 

db = SQLAlchemy(app)

from app import routes, models

@app.cli.command('init-db')
def init_db():

    # Create the database for the app from scratch
    db.drop_all()
    db.create_all()

    # Create equipment item records to populate db
    microbit = models.Equipment (
        equip_name  = 'Microbit',
        location_id = 'Library',
        purchase_price = 29.40,
        equip_quantity = 1,
        date_entered = '2021-04-04',
        equip_image = 'image.jpg'
    )
    db.session.add(microbit)

    
    beebot = models.Equipment (
        equip_name  = 'Beebot',
        location_id = 'C10',
        purchase_price = 5.40,
        equip_quantity = 10,
        date_entered = '2021-05-01',
        equip_image = 'image1.jpg'
    )
    db.session.add(beebot)

    # Create user item records to populate db
    person1 = models.User (
        first_name  = 'Kelly',
        last_name = 'Butler',
        email = 'butlerk@email.com',
        password = 'hello'
    )
    db.session.add(person1)

    
    person2 = models.User (
        first_name  = 'Kirsty',
        last_name = 'Watts',
        email = 'wattsk@email.com',
        password = 'goodbye'
    )
    db.session.add(person2)










    # Save the created records to the database file
    db.session.commit()
