from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Bike

class ContactForm(FlaskForm):
    message = TextAreaField('Message', render_kw={"rows": 5})
    submit = SubmitField('Send')
    
class CheckOutForm(FlaskForm):
    location = SelectField('Bike Location', choices=[(
        'ND', 'North Dorms'), ('APT', 'Apartments')], validators=[DataRequired()])
    submit = SubmitField('Check Out')

class CheckInForm(FlaskForm):
    location = SelectField('Bike Location', choices=[(
        'ND', 'North Dorms'), ('APT', 'Apartments')], validators=[DataRequired()])
    available_bikes = Bike.query.filter_by(status='available')

    # create a tuple of (bike, bike number) and add it to the drop down menu:
    choices = []
    for bike in available_bikes:
        choices.append((bike.id, bike.number))
    bike = SelectField('Bike Number', choices=choices,
                       validators=[DataRequired()], coerce=int)
    submit = SubmitField('Check In')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    honor_code_agreement = BooleanField(
        'Agree to abide by Honor Code using the program', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:    # check for duplicate emails
            raise ValidationError('Please use a different email address.')
        domain = email.data.split('@')[1]
        if domain != "haverford.edu":
            raise ValidationError('Please use your Haverford email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
