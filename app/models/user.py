from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import UserMixin
from time import time
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


subs = db.Table('subs',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('subreddit_id', db.Integer,
                          db.ForeignKey('subreddits.id')))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(50), unique=True)

    subscriptions = db.relationship(
        'Subreddit', secondary=subs,
        backref=db.backref('subscribers', lazy='dynamic'),
        lazy='dynamic')

    my_subreddits = db.relationship('Subreddit', backref='creator',
                                    lazy='dynamic')

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, email, username):
        self.email = email
        self.username = username

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def is_subscribed(self, subreddit):
        return self.subscriptions.filter(
            subs.c.subreddit_id == subreddit.id).count() > 0

    def subscribe(self, subreddit):
        if not self.is_subscribed(subreddit):
            self.subscriptions.append(subreddit)

    def unsubscribe(self, subreddit):
        if self.is_subscribed(subreddit):
            self.subscriptions.remove(subreddit)

    def __repr__(self):
        return '<User %r>' % (self.username)
