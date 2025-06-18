from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from .models import User # Assuming User model is in app/models.py

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)]) # Added max length
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email address is already registered. Please use a different one.')


class HardwareForm(FlaskForm):
    name = StringField('Hardware Name', validators=[DataRequired(), Length(max=100)])
    type = SelectField('Type', choices=[
        ('', '-- Select Type --'),
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Monitor', 'Monitor'),
        ('Printer', 'Printer'),
        ('Scanner', 'Scanner'),
        ('Router', 'Router'),
        ('Switch', 'Switch'),
        ('Server', 'Server'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[Optional(), Length(max=100)])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[Optional()])
    warranty_expiry_date = DateField('Warranty Expiry Date', format='%Y-%m-%d', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    status = SelectField('Status', choices=[
        ('En almacén', 'En almacén'), # In Stock
        ('En uso', 'En uso'),         # In Use
        ('En reparación', 'En reparación'), # Under Repair
        ('De baja', 'De baja')        # Decommissioned
    ], validators=[DataRequired()], default='En almacén')
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Add Hardware')

class SoftwareForm(FlaskForm):
    name = StringField('Software Name', validators=[DataRequired(), Length(max=100)])
    version = StringField('Version', validators=[Optional(), Length(max=50)])
    license_key = StringField('License Key', validators=[Optional(), Length(max=255)])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[Optional()])
    expiry_date = DateField('License Expiry Date', format='%Y-%m-%d', validators=[Optional()])
    seats = StringField('Number of Seats', validators=[Optional(), Length(max=10)]) # Using StringField for flexibility, can be converted to int in route
    installation_location = StringField('Installation Location', validators=[Optional(), Length(max=100)])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Add Software')
