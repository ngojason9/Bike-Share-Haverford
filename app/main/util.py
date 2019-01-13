from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps


def check_withholding(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.withholding == True:
            flash("You have withholding bike. Please check out before checking in again!")
            return redirect(url_for('main.timer'))
        return f(*args, **kwargs)

    return decorated_function