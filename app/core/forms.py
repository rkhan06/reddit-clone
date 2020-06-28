from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,\
    ValidationError


class PostForm(FlaskForm):

    title = StringField('Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    description = TextAreaField('Description', validators=[
        Length(min=0, max=500)
    ])
    community = SelectField('Choose Community', coerce=int,
                            default=0,
                            validators=[DataRequired()]
                            )

    def validate_community(self, community):
        if community.data == 0:
            raise ValidationError('Please Choose a Community')
