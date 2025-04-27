from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email

class ClientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[('', 'Select...'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = StringField('Contact Number')
    email = StringField('Email', validators=[Email()])
    address = TextAreaField('Address')
    programs = SelectMultipleField('Enroll in Programs', coerce=int)
    submit = SubmitField('Register Client')