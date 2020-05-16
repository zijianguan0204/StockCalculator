from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

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
    def amount_check(form, field):
            if field.data < 5000:
                raise ValidationError('The input amount must bigger or equal to 5000')

    input_amount = IntegerField('Input Dollor Amount',validators=[DataRequired(), amount_check])
    # invs_choices = [("Ethical Investing"), ("Growth Investing"), ("Index Investing"), ("Quality Investing"),("Value Investing")]
    # invs_method = SelectField(u'Investing Strategy', invs_choices)
    invs_method = StringField('Investing Strategy', validators=[DataRequired()])
    invs_method_opt = StringField('Second Investing Strategy')
    submit = SubmitField('Submit')

    