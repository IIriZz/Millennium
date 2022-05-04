# -*- coding: utf-8 -*-
# forms.py

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import (
    PasswordField,
    EmailField,
    SubmitField,
    StringField,
    BooleanField,
    TextAreaField,
)


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    r_password = PasswordField('Повтор пароля', validators=[DataRequired()])
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    submit = SubmitField('Продолжить')


class LoginForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    about_me = TextAreaField('about_me', validators=[Length(min = 0, max = 140)])
