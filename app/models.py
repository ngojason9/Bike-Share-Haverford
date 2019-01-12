from datetime import datetime
from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_bike = db.relationship('Bike', backref='last_bike', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[
                            'HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True, unique=True)
    status = db.Column(db.Enum('out of service', 'available', 'in use', name='status'), default='available')
    holder = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        if self.status == 'in use':
            return '<Bike #{}>, in use by {}>'.format(self.number, self.last_used_by.username)
        return '<Bike #{}>, status: {}>'.format(self.number, self.status)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
