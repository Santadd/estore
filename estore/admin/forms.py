from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, EqualTo, Length

class AdminRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
