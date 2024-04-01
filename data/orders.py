import sqlalchemy
from .db_session import SqlAlchemyBase

class PersonalOrder(SqlAlchemyBase):
    __tablename__ = 'admin_order'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    person = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    meal = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) #номер перемены
    status = sqlalchemy.Column(sqlalchemy.Boolean)
