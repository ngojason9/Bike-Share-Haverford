from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main import bp
from app.main.forms import CheckInForm, CheckOutForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Bike, Log
from werkzeug.urls import url_parse
from datetime import datetime, timedelta
from app.main.util import check_withholding


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
@login_required
@check_withholding
def index():
    form = CheckInForm()
    form.bike.choices = [(bike.id, bike.number)
                         for bike in Bike.query.filter_by(status='available')]

    if form.validate_on_submit():
        # Update Bike table
        bike = Bike.query.filter_by(id=form.bike.data).first()
        bike.status = 'in use'
        current_user.withholding = True

        # Update Log table
        db.session.add(Log(user=current_user.username,
                           bike=bike.number,
                           location_in=form.location.data,
                           check_in=datetime.now()))
        db.session.commit()

        flash('Congratulations, you are now checked in!')
        return redirect(url_for('main.timer'))

    return render_template("index.html", form=form)


@bp.route('/timer', methods=['GET', 'POST'])
@login_required
def timer():
    log = Log.query.filter_by(
        user=current_user.username, check_out=None).first()
    due_time = log.check_in + timedelta(hours=6)

    form = CheckOutForm()
    if form.validate_on_submit():
        # Update log table:
        log.location_out = form.location.data
        log.check_out = datetime.now()

        # Update bike table:
        bike = Bike.query.filter_by(number=log.bike).first()
        bike.status = "available"

        # Update user table:
        current_user.withholding = False

        db.session.commit()

        flash('Check out sucessfully!')
        return redirect(url_for('main.index'))

    return render_template('timer.html',
                           form=form,
                           check_in_time=log.check_in,
                           due_time=due_time,
                           seconds=int((due_time-datetime.now()).total_seconds()))


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
