import pickle
from datetime import datetime

from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user

from config.app_config import app, db, admin

# Таблица-связка для определения отношений между объектами Session и Question
questions_sessions = db.Table('questions_sessions',
                              db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
                              db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True)
                              )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, default='Unknown User')
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.today())
    sessions = db.relationship('Session', backref='user', lazy=True)
    role = db.Column(db.String(30), nullable=False, default='user')

    def __repr__(self):
        return f'<User {self.id}'


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', secondary=questions_sessions, lazy='subquery',
                                backref=db.backref('sessions', lazy=True))
    current_answer_num = db.Column(db.Integer, default=0)
    answers = db.Column(db.PickleType, nullable=True)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    wrong_answers = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, default=datetime.today())
    level = db.Column(db.Integer, nullable=False)

    def set_answers_list(self, data):
        self.answers = pickle.dumps(data)

    def get_answers_list(self):
        return pickle.loads(self.answers)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)


class UserView(ModelView):
    def is_accessible(self):
        return current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class SessionView(ModelView):
    column_exclude_list = ['answers', ]  # disable model deletion


admin.add_view(UserView(User, db.session))
admin.add_view(SessionView(Session, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
