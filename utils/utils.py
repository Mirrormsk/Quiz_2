import random
from random import shuffle, sample
from models.models_db import Question, User


def get_random_id() -> int:
    """
    Генерирует случайный id
    """
    digits = list('123456789')
    shuffle(digits)
    return int(''.join(digits))


def create_questions(diff_level: int, k: int = 10):
    """
    Функция для генерации списка вопросов
    :type k: int  - размер возвращаемого списка
    :param diff_level: принимает уровень сложности в виде int
    :return: возвращает список объектов класса Question
    """
    questions_all = Question.query.filter_by(level=diff_level).all()
    questions = random.sample(questions_all, k)
    return questions


def choose_plural(amount: int, declensions: tuple) -> str:
    """
    Принимает количество и формы слова в разном падеже.
    :return: возвращает строку в правильной форме
    """
    if amount % 10 == 1 and amount % 100 != 11:
        res = declensions[0]
    elif (amount % 10 in (2, 3, 4,)) and amount % 100 not in (12, 13, 14):
        res = declensions[1]
    else:
        res = declensions[2]
    return f'{amount} {res}'


def get_user_and_session(id_):
    """
    Возвращает объект юзера и последнюю сессию
    :param id_: int
    :return:
    todo: оформить аннотации типов
    """
    user = User.query.get(id_)
    if user:
        sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                                 reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
        if sorted_sessions:
            session = sorted_sessions[0]  # Получение последней сессии
            # Обработка последней сессии
        else:
            return f'У пользователя {User} пока нет сессий'
    else:
        return f'Пользователь с id {id_} не найден'
