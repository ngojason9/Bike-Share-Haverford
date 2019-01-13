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
    # available_bikes = Bike.query.filter_by(status='available')

    # create a tuple of (bike, bike number) and add it to the drop down menu:
    choices = []
    # for bike in available_bikes:
    #     choices.append((bike.id, bike.number))
    bike = SelectField('Bike Number', choices=choices,
                       validators=[DataRequired()], coerce=int)
    submit = SubmitField('Check In')
