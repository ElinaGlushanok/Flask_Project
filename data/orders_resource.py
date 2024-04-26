from flask import jsonify
from data import db_session
from data.static_data import *
from data.orders import PersonalOrder
from flask_restful import reqparse, abort, Resource


def abort_if_user_not_found(orders_id):
    session = db_session.create_session()
    orders = session.get(PersonalOrder, orders_id)
    if not orders:
        abort(404, message=f"Order {orders_id} not found")


class OrdersResource(Resource):
    def get(self, orders_id):
        abort_if_user_not_found(orders_id)
        session = db_session.create_session()
        orders = session.get(PersonalOrder, orders_id)
        return jsonify(
            {
                'orders': orders.to_dict(only=('id', 'person', 'meal', 'pause', 'status'))
            }
        )

    def delete(self, orders_id):
        abort_if_user_not_found(orders_id)
        session = db_session.create_session()
        orders = session.get(PersonalOrder, orders_id)
        session.delete(orders)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('person', required=True, type=int)
parser.add_argument('meal', required=True)
parser.add_argument('pause', required=True)
parser.add_argument('status', default=False)


class OrdersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(PersonalOrder).all()
        return jsonify(
            {
                'orders': [order.to_dict(only=('id', 'person', 'meal', 'pause', 'status'))
                          for order in orders]
            })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        meals_ordered = args['meal'].split(', ')
        meals = {elem.split('-')[0]: int(elem.split('-')[1]) for elem in meals_ordered}
        for i in meals.keys():
            if i.lower() not in meals_available:
                abort(400, message=f"Некорректно введены блюда")
        if len(set(meals.keys())) != len(meals.keys()):
            abort(400, message=f"Некорректно введены блюда")
        orders = PersonalOrder(
            person=args['person'],
            meal=args['meal'],
            pause=args['pause'],
            status=args['status']
        )
        session.add(orders)
        session.commit()
        return jsonify({'id': orders.id})