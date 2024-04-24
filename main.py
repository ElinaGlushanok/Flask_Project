import requests
import sqlite3
import logging

from data.users import User
from data.orders import PersonalOrder

from forms.login_form import LoginForm
from forms.new_order import NewOrderForm

from data import db_session

from flask_restful import Api
from flask import request, Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm
from forms.admin import RegisterAdminForm

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(application)
keyword = 'qwerty'
logging.basicConfig(filename='log_info.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

con = sqlite3.connect("db/canteen.db")
cur = con.cursor()
menu = list(cur.execute(f'''select * from menu''').fetchall())
meals_available = [x[1] for x in menu]
prices = {x[1]: x[2] for x in menu}


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
            print(1)
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
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
# toDo: same


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
        global keyword
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
                if i not in meals_available:
                    raise ValueError
            db_sess = db_session.create_session()
            orders = PersonalOrder(person=current_user.id, meal=add_form.meal.data, pause=add_form.pause.data)
            db_sess.add(orders)
            db_sess.commit()
            return redirect('/')
        except ValueError:
            return render_template('new_order.html', title='Создание заказа',
                                   form=add_form, message="Пожалуйста, вводите влюда только из меню")
        except Exception:
            return render_template('new_order.html',
                                   title='Создание заказа', form=add_form, message="Неверный формат ввода блюд")

    return render_template('new_order.html', title='Создание заказа', form=add_form, status=False)


@application.route("/show_menu")
def show_menu():
    return render_template("menu.html", meals=menu, title='Меню')


def main():
    try:
        api_url = 'https://random.imagecdn.app/v1/image?width=1000&height=300&category=food&format=json'
        photo = requests.get(api_url).json()
        img_data = requests.get(photo['url']).content
        with open('static/img/photo.jpg', 'wb') as handler:
            handler.write(img_data)
            handler.close()
            logging.info('API picture was got')
    except Exception as ex:
        logging.error(ex)
    finally:
        db_session.global_init("db/canteen.db")
        application.run()


if __name__ == '__main__':
    main()
