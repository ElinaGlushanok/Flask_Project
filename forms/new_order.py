from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, SubmitField


class NewOrderForm(FlaskForm):
    person = IntegerField('id')
    meal = StringField('Блюда (указывайте в формате "{блюдо}-{колличество}, {блюдо}-{колличество}... ")',
                       validators=[DataRequired()])
    pause = IntegerField('Номер перемены', validators=[DataRequired()])
    submit = SubmitField('Submit')
