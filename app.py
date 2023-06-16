from flask import request, render_template, redirect, jsonify, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from config.app_config import app, db, login_manager
from models.models_db import User, Session
from models.user_login import UserLogin
from utils.utils import get_random_id, create_questions, choose_plural, get_user_and_session


@app.route('/', methods=['POST', 'GET'])
def index():  # главная страница
    user = current_user

    if request.method == 'POST':
        # Получаем пользовательские данные из формы
        # todo: Сделать валидацию введенных данных
        selected_level = int(request.form['diff_level'])

        user = current_user

        # Создаем экземпляр сесcии с генерацией вопросов
        # todo: Запихнуть это в отдельную функцию и вынести в utils.py
        questions = create_questions(selected_level)
        user_session = Session(user_id=user.id, level=selected_level)
        user_session.questions.extend(questions)
        user_session.set_answers_list([])

        # Создаем объект пользователя
        # user = User(id=user_id,
        #             username=username,
        #             )

        db.session.add(user_session)
        # db.session.add(user)
        db.session.commit()

        return redirect(url_for('quiz'))
    else:
        return render_template('index.html', user=current_user)


@app.route('/quiz/', methods=['GET'])
@login_required
def quiz():  # put application's code here
    user = current_user

    sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                             reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
    if sorted_sessions:
        session = sorted_sessions[0]  # Получение последней сессии
        # Обработка последней сессии
    else:
        return f'У пользователя {User} пока нет сессий'

    # Если отвечены на все вопросы - перенаправление на статистику
    if session.current_answer_num == len(session.questions):
        return redirect(f'/stat/{session.id}')

    questions = session.questions

    curr_question = questions[session.current_answer_num]
    progress_percent = round(session.current_answer_num / len(questions) * 100)
    answer_length = choose_plural(len(curr_question.answer), ('буква', 'буквы', 'букв'))

    return render_template('quiz.html', question=curr_question, user=user, progress_percent=progress_percent,
                           answer_length=answer_length, user_session=session, user_id=user.id)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    user = current_user

    sorted_sessions = sorted(user.sessions, key=lambda session: session.id,
                             reverse=True)  # Сортировка сессий по полю 'id' в порядке убывания
    if sorted_sessions:
        session = sorted_sessions[0]  # Получение последней сессии
        # Обработка последней сессии
    else:
        return f'У пользователя {User} пока нет сессий'

    question = session.questions[session.current_answer_num]
    user_answer = request.form.get('user_answer').lower().strip()
    is_answer_correct = question.answer == user_answer
    if is_answer_correct:
        session.correct_answers += 1
    else:
        session.wrong_answers += 1

    session_answers = session.get_answers_list()
    session_answers.append((question, is_answer_correct))
    session.set_answers_list(session_answers)

    session.current_answer_num += 1
    db.session.commit()

    # print(is_answer_correct)
    return jsonify({'success': is_answer_correct})


@app.route('/stat/<int:session_id>')
@login_required
def stat(session_id):  # Страница статистики
    user = current_user
    session = Session.query.get(session_id)

    results = session.get_answers_list()
    correct_answers = len([res for qst, res in results if res])
    incorrect_answers = len(results) - correct_answers
    # print(f'Пользователь {user.username}: правильных {correct_answers}, неправильных {incorrect_answers}')
    return render_template('stat.html', user=user, correct_answers=correct_answers, incorrect_answers=incorrect_answers,
                           results=results, user_id=user.id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['user_email']).first()
        remember = True if request.form.get('remember') else False
        if user and check_password_hash(user.password, request.form['psw']):
            login_user(user, remember=remember)

            flash('Вы успешно вошли')
            return redirect(url_for('index'))
        flash('Неверно введены логин или пароль', 'error')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        user_email = request.form.get('user_email')
        user_password_1 = request.form.get('user_password_1')
        user_password_2 = request.form.get('user_password_2')

        if all(
                map(lambda x: len(x) > 3,
                    (username, user_email, user_password_1))) and user_password_1 == user_password_2 and all([username,
                                                                                                              user_password_1,
                                                                                                              user_password_2]):
            hash_psw = generate_password_hash(user_password_1)
            user = User(
                username=username,
                email=user_email,
                password=hash_psw
            )
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'Вы успешно зарегистрировались, {username}')
                return redirect(url_for('login'))
            except:
                flash(f'Ошибка регистрации', 'error')

        else:
            flash('Данные указаны неверно', 'error')

    else:
        return render_template('register.html', title='Регистрация')


@login_manager.user_loader
def load_user(user_id):
    # print("load_user")
    return User.query.get(user_id)


@app.route('/profile')
@login_required
def profile():  # Страница статистикиe

    sessions = []
    for session in current_user.sessions:
        results = session.get_answers_list()
        if results:
            correct_answers = len([res for qst, res in results if res])
            incorrect_answers = len(results) - correct_answers
            percent_of_correct_answers = round(correct_answers / len(results) * 100)
            difficulty_levels = ('Легкий', 'Средний', 'Тяжелый')

            session_data = {
                'id': session.id,
                'level': difficulty_levels[session.level - 1],
                'date': session.date.strftime('%Y-%m-%d %H:%M'),
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'percent_of_correct_answers': percent_of_correct_answers
            }

            sessions.append(session_data)
    return render_template('profile.html', user=current_user, sessions=sessions)


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response


if __name__ == '__main__':
    db.create_all()
    app.run()
