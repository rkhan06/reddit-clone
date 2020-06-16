from app import db
from datetime import datetime


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddits.id'))

    def __repr__(self):
        return '<Subreddit {}>'.format(self.id)
