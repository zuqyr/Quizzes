# Здесь будет код веб-приложения
from random import shuffle
from flask import Flask, session, redirect, request, url_for, render_template
from db_scripts import get_question_after, get_quises, check_answer
import os

folder = os.getcwd()

def start_quiz(quiz_id):
    '''создаёт нужные значения в словаре session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def index():
    ''' Первая страница: если пришли запросом GET, то выбрать викторину, 
    если POST - то запомнить id викторины и отправлять на вопросы'''
    if request.method == 'GET':
        # викторина не выбрана, сбрасываем id викторины и показываем форму выбора
        start_quiz(-1)
        return quiz_form()
    else:
        # получили дополнительные данные в запросе! Используем их:
        quest_id = request.form.get('quiz') # выбранный номер викторины 
        start_quiz(quest_id)
        return redirect(url_for('test'))

def test():
    if not ('quiz' in session) or int(session ['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method =="POST":
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result)==0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]
            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'

def result():
    return session['answers'], session['total']

def quiz_form():
    ''' функция получает список викторин из базы и формирует форму с выпадающим списком'''
    html_beg = '''<html><body><h2>Выберите викторину:</h2><form method="post" action="index"><select name="quiz">'''
    frm_submit = '''<p><input type="submit" value="Выбрать"> </p>'''

    html_end = '''</select>''' + frm_submit + '''</form></body></html>'''
    options = ''' '''
    q_list = get_quizzes()
    for id, name in q_list:
        option_line = ('''<option value="''' +
                        str(id) + '''">''' +
                        str(name) + '''</option>
                      ''')
        options = options + option_line
    return html_beg + options + html_end

def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html', question = question[1], quest_id = question[0], answers_list = answers_list)

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
            next_question = get_question_after(session['last_question'], session['quiz'])
            if next_question is None or len(next_question) == 0:
                return redirect(url_for('result'))
            else:
                return question_form(next_question)


app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index)   # создаёт правило для URL '/'
app.add_url_rule('/index', 'index', index, methods=['post', 'get']) # правило для '/index' 
app.add_url_rule('/test', 'test', test) # создаёт правило для URL '/test'
app.add_url_rule('/result', 'result', result) # создаёт правило для URL '/test'
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
    app.run()

