from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class TradeInputForm(FlaskForm):

    """Input form for receving trade details"""

    symbol = StringField('Symbol', validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    side = SelectField('Side', coerce=int, choices=[(1,'Buy'), (2, 'Sell')])
    trader_id = StringField('Trader ID', validators=[DataRequired()])
    submit = SubmitField('Submit Trade')
