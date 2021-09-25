from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length

#Flask form to add equipment to db
class AddEquipmentForm(FlaskForm):
    equip_name = StringField('Equipment name', validators=[InputRequired()])
    equip_quantity = IntegerField('Equipment Quantity', validators=[InputRequired()])
    location_id = IntegerField('Location', validators=[InputRequired()])
    equipment_price = IntegerField('Purchase Price', validators=[InputRequired()])
    equipment_date = StringField('Purchase Data')
    submit = SubmitField('Add equipment')

#Flask form to add location to db
class AddLocationForm(FlaskForm):
    location_name = StringField('Location name', validators=[InputRequired(), Length(min=1, max=40)])
    location_id = IntegerField('Location ID')
    submit = SubmitField('Add Location')

# Flask form to add user to db
class AddLocationForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=40)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=40)])
    email_address = StringField('Email address', validators=[InputRequired(), Length(min=1, max=40)])
    password = StringField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    user_id = StringField('User ID', validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField('Add User')