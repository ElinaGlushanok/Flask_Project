import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class PersonalOrder(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    person = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    meal = sqlalchemy.Column(sqlalchemy.String)
    pause = sqlalchemy.Column(sqlalchemy.Integer)  #номер перемены
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
