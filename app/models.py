from enum import unique
from sqlalchemy.orm import backref
from flask_login import UserMixin

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# Creating user, loan, equipment and location classes with associated fields/data types.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email_username = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text)
    loan = db.relationship('Loan', backref = 'user')
    is_admin = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key = True)
    location_name = db.Column(db.Text)
    equipment = db.relationship('Equipment', backref = 'location')

class Loan(db.Model):
    loan_id = db.Column(db.Integer, primary_key = True)
    loan_date = db.Column(db.Date)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    equip_id= db.Column(db.Integer, db.ForeignKey('equipment.equip_id'), nullable = False)
    active = db.Column(db.Boolean)
    
class Equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key = True)
    equip_name = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable = False)
    purchase_price = db.Column(db.Numeric(5,2))
    equip_details= db.Column(db.Text)
    date_entered = db.Column(db.Text)
    file = db.Column(db.Text)
    loan = db.relationship('Loan', backref = 'equipment')

