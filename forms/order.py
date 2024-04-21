from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddOrderForm(FlaskForm):
    person = IntegerField('Заказчик', validators=[DataRequired()])
    meal = StringField('Состав заказа', validators=[DataRequired()])
    pause = IntegerField('Номер перемены', validators=[DataRequired()])  # номер перемены
    status = BooleanField('Отдан')
    submit = SubmitField('Заказать')
