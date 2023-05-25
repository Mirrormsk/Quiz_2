from flask_sqlalchemy import SQLAlchemy
from config.app_config import app, db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.today())
    sessions = db.relationship('Session', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id}'


class Session(db.Model):
    __tablename__ = 'sesions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.relationship(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', lazy=True)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
