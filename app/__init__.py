from flask import Flask
from config import Config

# Flask Plug-ins
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# Error Handling
from logging.handlers import RotatingFileHandler
import os
import logging
from logging.handlers import SMTPHandler
from sqlalchemy import MetaData


app = Flask(__name__)

app.config.from_object(Config)


metadata = MetaData(
  naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }
)
db = SQLAlchemy(app, metadata=metadata)

# db = SQLAlchemy(app)
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

from app import routes, models, errors