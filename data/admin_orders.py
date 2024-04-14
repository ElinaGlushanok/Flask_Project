import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class AdminOrder(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'admin_order'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    customer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    meal = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guests = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hours = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # Указание времени в часах
    minutes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # Указание времени в минутах
    status = sqlalchemy.Column(sqlalchemy.Boolean)





