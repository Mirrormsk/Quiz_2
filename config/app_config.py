import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.environ['SECRET_KEY_QUIZ']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

db: SQLAlchemy = SQLAlchemy(app)

login_manager = LoginManager(app)



