from app import db

class Equipment(db.Model):
    equip_id = db.Column(db.Integer, primary_key = True)
    equip_name = db.Column(db.Text)
    location_id = db.Column(db.Text)
    purchase_price = db.Column(db.Float)
    equip_quantity = db.Column(db.Integer)
    date_entered = db.Column(db.Date)
    equip_image = db.Column(db.Text)
