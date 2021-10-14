from sqlalchemy.orm import backref
from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    loan = db.relationship('Loan', backref = 'user')

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key = True)
    location_name = db.Column(db.Text)
    equipment = db.relationship('Equipment', backref = 'location')

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key = True)
    loan_date = db.Column(db.Text)
    loan_return = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    equip_id= db.Column(db.Integer, db.ForeignKey('equipment.equip_id'), nullable = False)
    

class Equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key = True)
    equip_name = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable = False)
    purchase_price = db.Column(db.Float)
    equip_quantity = db.Column(db.Integer)
    date_entered = db.Column(db.Text)
    equip_image = db.Column(db.Text)
    loan = db.relationship('Loan', backref = 'equipment')