import requests

from data.users import User
from data.orders import PersonalOrder

from data import db_session

from flask_restful import Api
from flask import request, Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

application = Flask(name)
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
    return render_template("index.html", orders=orders, title='Заказы')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/canteen.db")


if name == 'main':
    main()
