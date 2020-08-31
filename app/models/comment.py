from app import db
from datetime import datetime

comment_upvotes = db.Table('comment_upvotes',
                           db.Column('comment_id', db.Integer,
                                     db.ForeignKey('comments.id')),
                           db.Column('user_id', db.Integer,
                                     db.ForeignKey('users.id')))

comment_downvotes = db.Table('comment_downvotes',
                             db.Column('comment_id', db.Integer,
                                       db.ForeignKey('comments.id')),
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('users.id')))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent_id = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    upvotes = db.relationship('User',
                              secondary='comment_upvotes',
                              lazy='dynamic')
    downvotes = db.relationship('User',
                                secondary='comment_downvotes',
                                lazy='dynamic')

    def is_upvoted(self, user):
        return self.upvotes.filter(
            comment_upvotes.c.user_id == user.id).count() > 0

    def upvote(self, user):
        if not self.is_upvoted(user):
            if self.is_downvoted(user):
                self.downvotes.remove(user)
            self.upvotes.append(user)
            return 1
        else:
            self.upvotes.remove(user)
            return 2

    def is_downvoted(self, user):
        return self.downvotes.filter(
            comment_downvotes.c.user_id == user.id).count() > 0

    def downvote(self, user):
        if not self.is_downvoted(user):
            if self.is_upvoted(user):
                self.upvotes.remove(user)
            self.downvotes.append(user)
            return 1
        else:
            self.downvotes.remove(user)
            return 2

    def votes(self):
        return self.upvotes.count() - self.downvotes.count()
