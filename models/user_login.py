from flask_login.mixins import UserMixin
from config.app_config import db
from models.models_db import User


class UserLogin(UserMixin):

    def __init__(self):
        self.__user = None

    # создает параметр __user - модель класса User
    def from_db(self, user_id, db_model: db.Model = User):
        self.__user: User = db_model.query.get(user_id)

    # Создает экземпляр класса UserLogin из экземпляра User
    def create(self, user):
        self.__user = user

    # Возвращает id пользователя в виде строки
    def get_id(self):
        return str(self.__user.id)
