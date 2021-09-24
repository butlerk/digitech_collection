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

    # Create an equipment item record
    microbit = models.Equipment (
        equip_name  = 'Microbit',
        location_id = 'Apple',
        purchase_price = 29.40,
        equip_quantity = 1,
        date_entered = 23/4/2021,
        equip_image = 'image.jpg'
    )
    db.session.add(microbit)

    # Save the created records to the database file
    db.session.commit()
