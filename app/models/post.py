from app import db
from datetime import datetime
from .comment import Comment


post_upvotes = db.Table('post_upvotes',
                        db.Column('post_id', db.Integer,
                                  db.ForeignKey('posts.id')),
                        db.Column('user_id', db.Integer,
                                  db.ForeignKey('users.id')))

post_downvotes = db.Table('post_downvotes',
                          db.Column('post_id', db.Integer,
                                    db.ForeignKey('posts.id')),
                          db.Column('user_id', db.Integer,
                                    db.ForeignKey('users.id')))


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddits.id'))
    upvotes = db.relationship('User', secondary='post_upvotes', lazy='dynamic')
    downvotes = db.relationship('User', secondary='post_downvotes',
                                lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def get_parent_comments(self):
        return self.comments.filter(
            Comment.parent_id == 0).all()

    def get_child_comments(self):
        return self.comments.filter(
            Comment.parent_id > 0).all()

    def is_upvoted(self, user):
        return self.upvotes.filter(
            post_upvotes.c.user_id == user.id).count() > 0

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
            post_downvotes.c.user_id == user.id).count() > 0

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

    def __repr__(self):
        return '<Subreddit {}>'.format(self.title)
