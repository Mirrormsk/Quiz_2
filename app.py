import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from flask import session

from utils.utils import get_random_id, create_questions, choose_plural
from static.data.words_dicts import words_base
from static.data.user_sessions import user_sessions
from models.models import UserSession, Question

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY_QUIZ']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'



@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        selected_level = int(request.form['diff_level'])
        username = request.form['username']
        user_id = get_random_id()
        # words = words_base[selected_level]
        user = UserSession(user_id=user_id,
                           username=username,
                           diff_level=selected_level)
        user.questions = create_questions(words_base[selected_level], 10)
        user_sessions[user_id] = user
        return redirect(f'/quiz/{user_id}')
    else:
        return render_template('index.html')


@app.route('/quiz/<int:id>', methods=['GET'])
def quiz(id):  # put application's code here
    user = user_sessions[id]
    # Если отвечены на все вопросы - перенаправление на статистику
    if user.current_answer_number == len(user.questions):
        return redirect(f'/stat/{user.user_id}', )

    curr_question = user.questions[user.current_answer_number]
    progress_percent = round(user.current_answer_number / len(user.questions) * 100)
    answer_length = choose_plural(len(curr_question.answer), ('буква', 'буквы', 'букв'))

    return render_template('quiz.html', question=curr_question, user=user, progress_percent=progress_percent,
                           answer_length=answer_length)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    user = user_sessions[int(request.form.get('user_id'))]
    question = user.questions[user.current_answer_number]
    user_answer = request.form.get('user_answer').lower()
    is_answer_correct = question.is_answered_correct(user_answer)
    if is_answer_correct:
        user.correct_answers += 1
    user.total_answers += 1
    user.answers.append((question, is_answer_correct))
    user.current_answer_number += 1
    # print(is_answer_correct)
    return jsonify({'success': is_answer_correct})


@app.route('/stat/<int:id>')
def stat(id):  # Страница статистики
    user = user_sessions[id]
    return render_template('stat.html', user=user)


if __name__ == '__main__':
    app.run()
