from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField, BooleanField, SubmitField


class NewOrderForm(FlaskForm):
    person = IntegerField('id', validators=[DataRequired()])
    meal = StringField('Блюда', validators=[DataRequired()])
    pause = IntegerField('Номер перемены', validators=[DataRequired()])
    submit = SubmitField('Submit')
