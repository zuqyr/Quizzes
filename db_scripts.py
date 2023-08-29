import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):  
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS questions'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )''')
    do('''CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
    )''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content(
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz(id),
        FOREIGN KEY (question_id) REFERENCES questions(id)
    )''')
    close()

def add_questions():
    questions = [
        ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
    ]
    open()
    cursor.executemany('''INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'no':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close()
    
def get_question_after(question_id, quiz_id):
    open()
    query = '''SELECT quiz_content.id, questions.question, questions.answer, questions.wrong1, questions.wrong2, questions.wrong3
    FROM questions, quiz_content 
    WHERE quiz_content.question_id == questions.id
    AND quiz_content.id > ?
    AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id'''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchall()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('questions')
    show('quiz')
    show('quiz_content')

def check_answer():
    query = '''SELECT question.answer
    FROM quiz_content, question
    WHERE quiz_content.id = ?
    AND quiz_content.question_id = question.id
    '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()
    #print(result)
    if result is None:
        return False # не нашли
    else:
        if result[0] == ans_text:
            # print(ans_text)
            return True # ответ совпал
        else:
            return False # нашли, но ответ не совпал

def get_quizzes():
    query = "SELECT * FROM quiz ORDER BY id"
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result
    
def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    print(get_question_after(3,1))

if __name__ == "__main__":
    main()

