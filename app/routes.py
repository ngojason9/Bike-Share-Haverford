from app.email import send_password_reset_email
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, CheckInForm, CheckOutForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Bike, Log
from werkzeug.urls import url_parse
from datetime import datetime, timedelta


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    form = CheckInForm()
    if form.validate_on_submit():
        # location = form.location.data

        bike = Bike.query.filter_by(id=form.bike.data)
        bike.status = 'in use'
        bike.last_used_by = current_user.id
        check_in_time = datetime.now()
        due_time = datetime.now() + timedelta(hours=6)

        db.session.commit()

        flash('Congratulations, you are now checked in!')

        return redirect(url_for('timer', check_in_time=check_in_time.strftime('%b %d, %Y %I:%M %p'), due_time=due_time.strftime('%b %d, %Y %I:%M %p')))

    return render_template("index.html", form=form)


@app.route('/timer', methods=['GET', 'POST'])
def timer():
    check_in_time = request.args.get('check_in_time')
    due_time = request.args.get('due_time')

    form = CheckOutForm()
    if form.validate_on_submit():
        flash('Check out sucessfully!')
        return redirect(url_for('index'))

    return render_template('timer.html', form=form, check_in_time=check_in_time, due_time=due_time, seconds=6*3600)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Thank you for your message!')
        return redirect(url_for('index'))
        
    return render_template('contact.html', form=form)