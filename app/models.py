from app import db

class Equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key = True)
    equip_name = db.Column(db.Text)
    location_id = db.Column(db.Text)
    purchase_price = db.Column(db.Float)
    equip_quantity = db.Column(db.Integer)
    date_entered = db.Column(db.Text)
    equip_image = db.Column(db.Text)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    