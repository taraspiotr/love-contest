from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    image_name = db.Column(db.String(128))
    rating = db.Column(db.Integer, default=1000)

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.surname)


class User(UserMixin, db.Model):
    """
    Create an Employee table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    image_name = db.Column(db.String(128))
    rating = db.Column(db.Integer, default=1000)    
    is_admin = db.Column(db.Boolean, default=False)
    
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {} {}>'.format(self.first_name, self.last_name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    winner_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('contestant.id'))

    def __repr__(self):
        return '<Voted {} over {}>'.format(self.winner_id, self.loser_id) 
