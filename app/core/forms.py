from wtforms.validators import DataRequired, Length,\
    ValidationError, URL
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, \
    SubmitField


class PostForm(FlaskForm):

    title = StringField('Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    description = TextAreaField('Description', validators=[
        Length(min=0, max=2000)
    ])
    community = SelectField(
        'Choose Community', coerce=int,
        default=0,
        validators=[DataRequired()]
    )
    submit = SubmitField('create a Post')

    def validate_community(self, community):
        if community.data == 0:
            raise ValidationError('Please Choose a Community')


class ImageForm(FlaskForm):

    title = StringField('Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    image = FileField('Add File', validators=[DataRequired()])
    community = SelectField(
        'Choose Community', coerce=int,
        default=0,
        validators=[DataRequired()]
    )
    imagesubmit = SubmitField('create a Post')

    def validate_community(self, community):
        if community.data == 0:
            raise ValidationError('Please Choose a Community')


class LinkForm(FlaskForm):

    title = StringField('Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    link = StringField('Link', validators=[
        DataRequired(),
        Length(min=0, max=500),
        URL('Invalid url.')
    ])
    community = SelectField(
        'Choose Community', coerce=int,
        default=0,
        validators=[DataRequired()]
    )
    submit = SubmitField('create a Post')

    def validate_community(self, community):
        if community.data == 0:
            raise ValidationError('Please Choose a Community')
