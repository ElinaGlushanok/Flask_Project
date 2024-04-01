from flask import Flask
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/canteen.sqlite")
    app.run()

if __name__ == '__main__':
    main()

    #https://github.com/SergeEvdokimov/Flask_project.git