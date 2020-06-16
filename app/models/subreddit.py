from app import db
# from flask import current_app
from datetime import datetime


class Subreddit(db.Model):

    __tablename__ = "subreddits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts = db.relationship('Post', backref='subreddit', lazy='dynamic')

    def __repr__(self):
        return '<Subreddit {}>'.format(self.name)
