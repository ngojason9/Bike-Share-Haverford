from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app.models import User, Bike


class ContactForm(FlaskForm):
    message = TextAreaField('Message', render_kw={
                            "rows": 5}, validators=[DataRequired()])
    submit = SubmitField('Send')
