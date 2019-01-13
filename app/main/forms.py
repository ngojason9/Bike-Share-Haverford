from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
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
    bike = SelectField('Bike Number', choices=[],
                       validators=[DataRequired()], coerce=int)
    submit = SubmitField('Check In')