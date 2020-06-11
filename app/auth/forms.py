from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,\
    BooleanField
from wtforms.validators import DataRequired, Length, EqualTo,\
    ValidationError, Email
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=3)
    ])
    remember_me = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(), EqualTo('password')
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email address has not been registered')


class PasswordChangeForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
