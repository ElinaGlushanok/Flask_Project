import requests

from data.db_session import create_session
from data.users import User
from data.orders import PersonalOrder

from forms.login_form import LoginForm

from data import db_session

from flask_restful import Api
from flask import request, Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.order import AddOrderForm
from forms.user import RegisterForm

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(application)


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
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route("/")
@application.route("/index")
def index():
    db_sess = db_session.create_session()
    orders = {order.id: (order.person, order.meal, order.pause, order.status)
              for order in db_sess.query(PersonalOrder).all()}
    return render_template("index.html", orders=orders, title='Заказы') #[order.person][0]


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.surname == form.surname.data,
                                      User.name == form.name.data,
                                      User.grade == form.grade.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, surname=form.surname.data, grade=form.grade.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Форма регистрации', form=form)


@application.route('/addorder', methods=['GET', 'POST'])
def new_job():
    add_form = AddOrderForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        orders = PersonalOrder(person=add_form.person.data, meal=add_form.meal.data, pause=add_form.pause.data,
                               status=add_form.status.data, is_finished=add_form.is_finished.data,
                               category=add_form.category.data)
        db_sess.add(orders)
        db_sess.commit()
        return redirect('/')
    return render_template('new_order.html', title='Создание заказа', form=add_form)


def main():
    db_session.global_init("db/canteen.db")
    application.run()


if __name__ == '__main__':
    main()
