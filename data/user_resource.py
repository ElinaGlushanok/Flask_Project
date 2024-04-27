from flask import jsonify
from data import db_session
from data.users import User
from flask_restful import reqparse, abort, Resource


def abort_if_user_not_found(users_id):
    session = db_session.create_session()
    users = session.get(User, users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        users = session.get(User, users_id)
        if users.grade != '-':
            return jsonify(
                {
                    'users': users.to_dict(only=('id', 'surname', 'name', 'grade'))
                }
            )
        abort(404, message=f"User {users_id} not found")

    def delete(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        users = session.get(User, users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('grade', required=True)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [user.to_dict(only=('id', 'surname', 'name', 'grade'))
                          for user in users if user.grade != '-']
            })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            grade=args['grade']
        )
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})