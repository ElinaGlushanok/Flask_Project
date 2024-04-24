from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import BooleanField, SubmitField, StringField


class DeleteOrderForm(FlaskForm):
    key_word = StringField('Кодовое слово', validators=[DataRequired()])
    status = BooleanField('Вы уверены, что хотите удалить заказ?', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
