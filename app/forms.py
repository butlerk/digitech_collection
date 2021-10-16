from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, PasswordField 
from wtforms.fields.core import DateTimeField, SelectField
from wtforms.validators import InputRequired, Length
from datetime import datetime

from wtforms.widgets.core import CheckboxInput



#Flask form to add equipment to db
class AddEquipmentForm(FlaskForm):
    equip_name = StringField('Equipment name', validators=[InputRequired()])
    equip_quantity = IntegerField('Equipment Quantity', validators=[InputRequired()])
    available = CheckboxInput('available')
    location_id = SelectField(u'Location', coerce = int)
    purchase_price = IntegerField('Purchase Price', validators=[InputRequired()])
    date_entered = StringField('Purchase Date')
    equip_image = StringField('Equipment Image')
    submit = SubmitField('Add equipment')

# Flask form to add loacation to db
class AddLocationForm(FlaskForm):
    location_name = StringField('Location name')
    #location_id = IntegerField('Location ID')
    submit = SubmitField('Add Location')

# Flask form to add user to db
class AddUserForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=40)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email address', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    submit = SubmitField('Add User')

# Flask form to add loan to db
class AddLoanForm(FlaskForm):
    loan_id = IntegerField('Loan ID')
    loan_date = DateTimeField('Date borrowed')
    user_id = SelectField(u'Loan by',coerce=int)
    equip_id = SelectField(u'Equipment borrowed',coerce=int)
    submit = SubmitField('Add Loan')

class EditUserForm(AddUserForm):
    submit = SubmitField('Save User')

class EditEquipmentForm(AddEquipmentForm):
    submit = SubmitField('Save Equipment')

class EditLocationForm(AddLocationForm):
    submit = SubmitField('Save Location')

class EditLoanForm(AddLoanForm):
    submit = SubmitField('Save Loan')
