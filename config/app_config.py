import os

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ['SECRET_KEY_QUIZ']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db: SQLAlchemy = SQLAlchemy(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Панель администратора', template_mode='bootstrap4')

login_manager = LoginManager(app)
