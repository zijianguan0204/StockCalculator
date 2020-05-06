from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

class realTimeInfoForm(FlaskForm):
    symbol = StringField('Stock Symbol',
                         validators=[DataRequired()])
    submit = SubmitField('Calculate')

class invsForm(FlaskForm):
    input_amount = IntegerField('Input Dollor Amount',validators=[DataRequired()])
    # invs_choices = [("Ethical Investing"), ("Growth Investing"), ("Index Investing"), ("Quality Investing"),("Value Investing")]
    # invs_method = SelectField(u'Investing Strategy', invs_choices)
    invs_method = StringField('Investing Strategy', validators=[DataRequired()])
    submit = SubmitField('Submit')
