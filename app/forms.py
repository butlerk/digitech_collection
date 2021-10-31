from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, PasswordField, DecimalField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import InputRequired, Length
from datetime import datetime
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.widgets.core import CheckboxInput



#Flask form to add equipment to db

class LoginForm(FlaskForm):
    email_username = StringField('Username:', validators=[InputRequired(), Length(1, 64)])
    password = PasswordField('Password:', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class AddEquipmentForm(FlaskForm):
    equip_name = StringField('Equipment name', validators=[InputRequired()])
    equip_quantity = IntegerField('Equipment Quantity', validators=[InputRequired()])
    location_id = SelectField(u'Location', coerce = int)
    purchase_price =StringField('Purchase Price', validators=[InputRequired()])
    date_entered = StringField('Purchase Date')
    file = FileField('file')
    submit = SubmitField('Add equipment')


# Flask form to add locations to db
class AddLocationForm(FlaskForm):
    location_name = StringField('Location name')
    #location_id = IntegerField('Location ID')
    submit = SubmitField('Add Location')

# Flask form to add user to db
class AddUserForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=1, max=40)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=1, max=40)])
    email_username = StringField('Email address', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    is_admin = BooleanField('Admin?')
    submit = SubmitField('Add User')
    

# Flask form to add loan to db
class AddLoanForm(FlaskForm):
    loan_id = IntegerField('Loan ID')
    loan_date = DateField('Loan Date ie. 27-03-2021',format='%d-%m-%Y')
    id = SelectField(u'Loan by',coerce=int)
    equip_id = SelectField(u'Equipment borrowed',coerce=int)
    submit = SubmitField('Add Loan')

class PhotoForm(FlaskForm):
   
    submit = SubmitField('Upload Photo')

# Flask form to edit user inheriting from Add User form
class EditUserForm(AddUserForm):
    submit = SubmitField('Save User')

# Flask form to edit equipment inheriting from Add Equipment form
class EditEquipmentForm(AddEquipmentForm):
    submit = SubmitField('Save Equipment')

# Flask form to edit location inheritig from Add Location form
class EditLocationForm(AddLocationForm):
    submit = SubmitField('Save Location')

# Flask form to edit loan inheritig from Add Loan form
class EditLoanForm(AddLoanForm):
    submit = SubmitField('Save Loan')




