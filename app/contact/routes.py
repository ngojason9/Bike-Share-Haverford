from app.email import send_email
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.contact import bp
from app.contact.forms import ContactForm
from app.models import User
from flask_login import current_user
from werkzeug.urls import url_parse

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email('[Bikeshare] Contact Form Submission', sender=current_app.config['ADMINS'][0], recipients=['ngojason9@gmail.com'], text_body=render_template(
        'contact/contact_email.txt', body=form.message.data, user=current_user), html_body=render_template('contact/contact_email.html', body=form.message.data, user=current_user))

        flash('Thank you for your message!')
        return redirect(url_for('main.index'))

    return render_template('contact/contact.html', form=form)
