import sqlalchemy
from .db_session import SqlAlchemyBase

class AdminOrder(SqlAlchemyBase):
    __tablename__ = 'admin_order'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    customer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    meal = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guests = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # Указание времени в часах
    status = sqlalchemy.Column(sqlalchemy.Boolean)





