import requests
import logging

from data.users import User
from data.orders import PersonalOrder

from forms.login_form import LoginForm
from forms.new_order import NewOrderForm

from data import db_session
from data.static_data import *

from flask_restful import Api
from flask import request, Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm
from forms.admin import RegisterAdminForm
from forms.delete_order import DeleteOrderForm

from data.user_resource import UsersResource, UsersListResource
from data.admin_resource import AdminsResource, AdminsListResource
from data.orders_resource import OrdersResource, OrdersListResource

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(application)


login_manager = LoginManager()
login_manager.init_app(application)
logging.basicConfig(filename='log_info.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

db_session.global_init("db/canteen.db")

api.add_resource(UsersListResource, '/api/v2/users')
api.add_resource(UsersResource, '/api/v2/users/<int:users_id>')
api.add_resource(AdminsListResource, '/api/v2/admins')
api.add_resource(AdminsResource, '/api/v2/admins/<int:admins_id>')
api.add_resource(OrdersListResource, '/api/v2/orders')
api.add_resource(OrdersResource, '/api/v2/orders/<int:orders_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.surname == form.surname.data,
                                          User.name == form.name.data,
                                          User.grade == form.grade.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            logging.info(f'user {current_user} logged in')
            return redirect("/")
        return render_template('login.html', message="Неверно введена информация пользователя", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route("/")
@application.route("/index")
def index():
    db_sess = db_session.create_session()
    data = [order for order in db_sess.query(PersonalOrder).all()]
    orders = []
    for elem in data:
        summ = 0
        meal_count = {}
        for name_count in elem.meal.split(', '):
            meal_count[name_count.split('-')[0]] = int(name_count.split('-')[1])
            summ += prices[name_count.split('-')[0]] * int(name_count.split('-')[1])
        orders.append([elem.id, elem.person, ', \n'.join([f'{x} {y} (шт./порц.)' for x, y in meal_count.items()]),
                       summ, elem.pause, elem.status])
    return render_template("index.html", orders=orders, title='Заказы')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_user.html', title='Регистрация', form=form, message="Пароли не совпадают")
        if form.grade.data == '-':
            return render_template('register_user.html', title='Регистрация', form=form, message="Некорректный класс")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.surname == form.surname.data,
                                      User.name == form.name.data,
                                      User.grade == form.grade.data).first():
            return render_template('register_user.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, surname=form.surname.data, grade=form.grade.data, admin=False)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_user.html', title='Форма регистрации', form=form)


@application.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = RegisterAdminForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_admin.html',
                                   title='Регистрация', form=form, message="Пароли не совпадают")
        if form.key_word.data != keyword:
            return render_template('register_admin.html',
                                   title='Регистрация', form=form, message="Неверное кодовое слово")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.surname == form.surname.data,
                                      User.name == form.name.data,
                                      User.grade == '-').first():
            return render_template('register_admin.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, surname=form.surname.data, grade='-', admin=True)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_admin.html', title='Форма регистрации', form=form)


@application.route('/add_order', methods=['GET', 'POST'])
def new_order():
    add_form = NewOrderForm()
    if add_form.validate_on_submit():
        try:
            meals_ordered = add_form.meal.data.split(', ')
            meals = {elem.split('-')[0]: int(elem.split('-')[1]) for elem in meals_ordered}
            for i in meals.keys():
                if i.lower() not in meals_available:
                    raise ValueError
            if len(set(meals.keys())) != len(meals.keys()):
                raise NameError
            db_sess = db_session.create_session()
            orders = PersonalOrder(person=current_user.id, meal=add_form.meal.data, pause=add_form.pause.data,
                                   status=add_form.status.data)
            db_sess.add(orders)
            db_sess.commit()
            return redirect('/')
        except ValueError:
            return render_template('new_order.html', title='Создание заказа', meals=menu,
                                   form=add_form, message="Пожалуйста, вводите блюда только из меню")
        except NameError:
            return render_template('new_order.html', title='Создание заказа', meals=menu,
                                   form=add_form, message="Пожалуйста, не вводите одинаковые блюда несколько раз")
        except Exception:
            return render_template('new_order.html', meals=menu,
                                   title='Создание заказа', form=add_form, message="Неверный формат ввода блюд")

    return render_template('new_order.html', title='Создание заказа', form=add_form, meals=menu,)


@application.route("/show_menu")
def show_menu():
    return render_template("menu.html", meals=menu, title='Меню')


@application.route('/orders/<int:unic_num>', methods=['GET', 'POST'])
@login_required
def order_edit(unic_num):
    form = NewOrderForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        orders = db_sess.query(PersonalOrder).filter(PersonalOrder.id == unic_num).first()
        if not orders or not current_user.admin:
            abort(404)
        form.meal.data = orders.meal
        form.pause.data = orders.pause
        form.status.data = orders.status
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        orders = db_sess.query(PersonalOrder).filter(PersonalOrder.id == unic_num).first()
        if orders and current_user.admin:
            orders.meal = form.meal.data
            orders.team_leader = form.pause.data
            orders.status = form.status.data
            db_sess.commit()
            return redirect('/')
        abort(404)
    return render_template('new_order.html', title='Изменение заказа', form=form, meals=menu,)


@application.route('/delete_order/<int:unic_num>', methods=['GET', 'POST'])
@login_required
def delete_order(unic_num):
    form = DeleteOrderForm()
    if form.validate_on_submit():
        if form.key_word.data != keyword:
            return render_template('delete_order.html',
                                   title='Удаление заказа', form=form, message="Неверно введено кодовое слово")
        db_sess = db_session.create_session()
        orders = db_sess.query(PersonalOrder).filter(PersonalOrder.id == unic_num).first()
        if not orders or not current_user.admin:
            abort(404)
        db_sess.delete(orders)
        db_sess.commit()
        return redirect('/')
    return render_template('delete_order.html', title='Удаление заказа', form=form)


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@application.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    try:
        width = 1000
        height = 300
        api_url = f'https://random.imagecdn.app/v1/image?width={width}&height={height}&category=food&format=json'
        photo = requests.get(api_url).json()
        img_data = requests.get(photo['url']).content
        with open('static/img/photo.jpg', 'wb') as handler:
            handler.write(img_data)
            handler.close()
            logging.info('API picture was got')
    except Exception as ex:
        logging.error(ex)
    finally:
        application.run(host='0.0.0.0')
