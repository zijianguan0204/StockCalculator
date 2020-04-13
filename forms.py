from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CalculateForm(FlaskForm):
    symbol = StringField('Stock Symbol',
                         validators=[DataRequired()])
    allotment = IntegerField('Allotment', validators=[DataRequired()])
    final_share_price = IntegerField('Final Share Price', validators=[DataRequired()])
    sell_commission = IntegerField('Sell Commission', validators=[DataRequired()])
    initial_share_price = IntegerField('Initial Share Price', validators=[DataRequired()])
    buy_commission = IntegerField('Buy Commission', validators=[DataRequired()])
    tax = FloatField('Tax', validators=[DataRequired()])
    submit = SubmitField('Calculate')
