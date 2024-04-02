from flask import Flask
from data import db_session

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/canteen.db")


if __name__ == '__main__':
    main()
