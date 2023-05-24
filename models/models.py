# from flask_sqlalchemy import SQLAlchemy
#
# db: SQLAlchemy = SQLAlchemy(app)


class Question:
    """
    Класс вопроса
    """

    def __init__(self, question: str, answer: str):
        self.question: str = question
        self.answer: str = answer

    def is_answered_correct(self, user_answer: str) -> bool:
        return user_answer.lower().strip() == self.answer


class UserSession():
    """
    Класс пользователя
    """

    def __init__(self, user_id, diff_level=1, username='Unknown Player', ):
        self.username = username.capitalize()
        self.user_id = user_id
        self.diff_level = diff_level
        self.answers: list[
            tuple[Question, bool]] = []  # список хранит пары из объектов Question и bool - верный ли ответ
        self.current_answer_number = 0
        self.total_answers: int = 0
        self.correct_answers: int = 0
        self.questions: list[Question] = []
