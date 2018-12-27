from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask

# Error Handling
from logging.handlers import RotatingFileHandler
import os
import logging
from logging.handlers import SMTPHandler

from flask_mail import Mail

from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bikeshare.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Bikeshare Haverford')

from flask_moment import Moment
moment = Moment(app)

from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from app import routes, models, errors
