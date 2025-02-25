import bcrypt

from flask_login import UserMixin

from database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    _password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean, nullable=False, default=True)
    token = db.Column(db.String(255), nullable=False)

    @property
    def is_active(self):
        return self.active

    @property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self._password_hash = password_hash.decode('utf8')

    def authenticate(self, password):
        return bcrypt.checkpw(password=password.encode('utf8'), hashed_password=self._password_hash.encode('utf8'))
