from flask import render_template, flash, redirect, url_for, request
from app import db
from app.main import bp
from app.main.forms import CheckInForm, CheckOutForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Bike, Log
from werkzeug.urls import url_parse
from datetime import datetime, timedelta


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    form = CheckInForm()
    available_bikes = Bike.query.filter_by(status='available')
    choices = []
    for bike in available_bikes:
        choices.append((bike.id, bike.number))
    form.bike.choices = choices

    if form.validate_on_submit():
        # location = form.location.data

        bike = Bike.query.filter_by(id=form.bike.data)
        bike.status = 'in use'
        bike.last_used_by = current_user.id
        check_in_time = datetime.now()
        due_time = datetime.now() + timedelta(hours=6)

        db.session.commit()

        flash('Congratulations, you are now checked in!')

        return redirect(url_for('main.timer', check_in_time=check_in_time.strftime('%b %d, %Y %I:%M %p'), due_time=due_time.strftime('%b %d, %Y %I:%M %p')))

    return render_template("index.html", form=form)


@bp.route('/timer', methods=['GET', 'POST'])
def timer():
    check_in_time = request.args.get('check_in_time')
    due_time = request.args.get('due_time')

    form = CheckOutForm()
    if form.validate_on_submit():
        flash('Check out sucessfully!')
        return redirect(url_for('main.index'))

    return render_template('timer.html', form=form, check_in_time=check_in_time, due_time=due_time, seconds=6*3600)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Thank you for your message!')
        return redirect(url_for('main.index'))

    return render_template('contact.html', form=form)
