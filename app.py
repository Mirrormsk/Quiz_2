from config.app_config import app, db

from flask import request, render_template, redirect, jsonify

from utils.utils import get_random_id, create_questions, choose_plural
from static.data.user_sessions import user_sessions
from models.models_db import User, Session, Question


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        # Получаем пользовательские данные из формы
        # todo: Сделать валидацию введенных данных
        selected_level = int(request.form['diff_level'])
        username = request.form['username']
        user_id = get_random_id()

        # Создаем экземпляр сесии с генерацией вопросов
        # todo: Запихнуть это в отдельную функцию и вынести в utils.py
        questions = create_questions(selected_level)
        user_session = Session(user_id=user_id)
        user_session.questions.extend(questions)
        user_session.set_answers_list([])

        # Создаем объект пользователя
        user = User(id=user_id,
                    username=username,
                    )

        db.session.add(user_session)
        db.session.add(user)
        db.session.commit()

        return redirect(f'/quiz/{user_id}')
    else:
        return render_template('index.html')


@app.route('/quiz/<int:id>', methods=['GET'])
def quiz(id):  # put application's code here
    user = User.query.get(id)
    if user:
        sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                                 reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
        if sorted_sessions:
            session = sorted_sessions[0]  # Получение последней сессии
            # Обработка последней сессии
        else:
            return f'У пользователя {User} пока нет сессий'
    else:
        return f'Пользователь с id {id} не найдет'

    # Если отвечены на все вопросы - перенаправление на статистику
    if session.current_answer_num == len(session.questions):
        return redirect(f'/stat/{user.id}', )

    questions = session.questions

    curr_question = questions[session.current_answer_num]
    progress_percent = round(session.current_answer_num / len(questions) * 100)
    answer_length = choose_plural(len(curr_question.answer), ('буква', 'буквы', 'букв'))

    return render_template('quiz.html', question=curr_question, user=user, progress_percent=progress_percent,
                           answer_length=answer_length, user_session=session, user_id=user.id)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    user = User.query.get(int(request.form.get('user_id')))
    if user:
        sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                                 reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
        if sorted_sessions:
            session = sorted_sessions[0]  # Получение последней сессии
            # Обработка последней сессии

        else:
            return f'У пользователя {user} пока нет сессий'
    else:
        return f'Пользователь с id {id} не найден'

    question = session.questions[session.current_answer_num]
    user_answer = request.form.get('user_answer').lower().strip()
    is_answer_correct = question.answer == user_answer
    # if is_answer_correct:
    #     user.correct_answers += 1

    session_answers = session.get_answers_list()
    session_answers.append((question, is_answer_correct))
    session.set_answers_list(session_answers)

    session.current_answer_num += 1
    db.session.commit()

    # print(is_answer_correct)
    return jsonify({'success': is_answer_correct})


@app.route('/stat/<int:id>')
def stat(id):  # Страница статистики
    user = User.query.get(id)
    if user:
        sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                                 reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
        if sorted_sessions:
            session = sorted_sessions[0]  # Получение последней сессии
            # Обработка последней сессии
        else:
            return f'У пользователя {user} пока нет сессий'
    else:
        return f'Пользователь с id {id} не найден'

    results = session.get_answers_list()
    correct_answers = len([res for qst, res in results if res])
    incorrect_answers = len(results) - correct_answers
    print(f'Пользователь {user.username}: правильных {correct_answers}, неправильных {incorrect_answers}')
    return render_template('stat.html', user=user, correct_answers=correct_answers, incorrect_answers=incorrect_answers,
                           results=results, user_id=user.id)


if __name__ == '__main__':
    db.create_all()
    app.run()
