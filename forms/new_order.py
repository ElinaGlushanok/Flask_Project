from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, SubmitField, BooleanField


class NewOrderForm(FlaskForm):
    person = IntegerField('id')
    meal = StringField('Блюда (указывайте в формате "{блюдо}-{количество}, {блюдо}-{количество}... ")',
                       validators=[DataRequired()])
    pause = IntegerField('Номер перемены', validators=[DataRequired()])
    status = BooleanField('Отдан')
    submit = SubmitField('Подтвердить')
