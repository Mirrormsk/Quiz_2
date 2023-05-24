from random import shuffle, sample
from models.models import Question


def get_random_id() -> int:
    """
    Генерирует случайный id
    """
    digits = list('123456789')
    shuffle(digits)
    return int(''.join(digits))


def create_questions(questions: dict[str, str], qst_number=10) -> list[Question]:
    """
    Принимает на вход словарь с вопросами, и возвращает
    объект Question
    :param qst_number:
    :param questions:
    :return:
    """
    words = sample(list(questions.keys()), qst_number)
    user_questions = [Question(word, questions[word].split(',')[0]) for word in words]
    return user_questions


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
