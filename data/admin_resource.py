from flask import jsonify
from data import db_session
from data.users import User
from data.static_data import keyword
from flask_restful import reqparse, abort, Resource


def abort_if_user_not_found(admins_id):
    session = db_session.create_session()
    users = session.get(User, admins_id)
    if not users:
        abort(404, message=f"Admin {admins_id} not found")


class AdminsResource(Resource):
    def get(self, admins_id):
        abort_if_user_not_found(admins_id)
        session = db_session.create_session()
        users = session.get(User, admins_id)
        print(users)
        if users.grade == '-':
            return jsonify(
                {
                    'admins': users.to_dict(only=('id', 'surname', 'name'))
                }
            )
        abort(404, message=f"Admin {admins_id} not found")

    def delete(self, admins_id):
        abort_if_user_not_found(admins_id)
        session = db_session.create_session()
        users = session.get(User, admins_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('keyword', required=True)


class AdminsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'admins': [user.to_dict(only=('id', 'surname', 'name'))
                           for user in users if user.grade == '-']
            })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if args['keyword'] != keyword:
            abort(400, message='Неверное кодовое слово')
        users = User(
            surname=args['surname'],
            name=args['name'],
            grade='-'
        )
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})