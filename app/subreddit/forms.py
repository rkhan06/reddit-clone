from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length,\
    ValidationError

from app.models.subreddit import Subreddit


class CreateCommunityForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired(), Length(min=2, max=50)])

    def validate_name(self, name):
        sub = Subreddit.query.filter_by(name=name.data).first()
        if sub is not None:
            raise ValidationError('A subreddit with this name already exists')


class EmptyForm(FlaskForm):
    submit = SubmitField()


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=2, max=50)])
