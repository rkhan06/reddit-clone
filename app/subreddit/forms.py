from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length,\
    ValidationError

from app.models.subreddit import Subreddit


class CreateCommunityForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired()])

    def validate_name(self, name):
        sub = Subreddit.query.filter_by(name=name.data).first()
        if sub is not None:
            raise ValidationError('A subreddit with this name already exists')


class PostForm(FlaskForm):
    post_text = TextAreaField('Post', validators=[
        DataRequired(),
        Length(min=1, max=200)
    ])
