import sqlite3

db_name = 'quiz.sqlite'

def get_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def get_quizes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz ORDER BY id")
        return cursor.fetchall()

def get_question_after(last_id, quiz_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT qc.id, q.question, q.answer, q.wrong1, q.wrong2, q.wrong3
        FROM question q
        JOIN quiz_content qc ON q.id = qc.question_id
        WHERE qc.quiz_id = ? AND qc.id > ?
        ORDER BY qc.id LIMIT 1
        ''', (quiz_id, last_id))
        return cursor.fetchone()

def check_answer(question_id, user_answer):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT q.answer FROM question q
        JOIN quiz_content qc ON q.id = qc.question_id
        WHERE qc.id = ?
        ''', (question_id,))
        result = cursor.fetchone()
        return result['answer'] == user_answer if result else False

def get_questions_count(quiz_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM quiz_content WHERE quiz_id = ?', (quiz_id,))
        return cursor.fetchone()[0]

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.executescript('''
        DROP TABLE IF EXISTS quiz_content;
        DROP TABLE IF EXISTS question;
        DROP TABLE IF EXISTS quiz;
        
        CREATE TABLE quiz (
            id INTEGER PRIMARY KEY,
            name VARCHAR
        );
        
        CREATE TABLE question (
            id INTEGER PRIMARY KEY,
            question VARCHAR,
            answer VARCHAR,
            wrong1 VARCHAR,
            wrong2 VARCHAR,
            wrong3 VARCHAR
        );
        
        CREATE TABLE quiz_content (
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (quiz_id) REFERENCES quiz (id),
            FOREIGN KEY (question_id) REFERENCES question (id)
        );
        ''')
        

        questions = [
            ('Первая коммерческая видеоигра?', 'Pong', 'Tetris', 'Space Invaders', 'Pac-Man'),
            ('Год выхода NES?', '1983', '1985', '1980', '1987'),
            ('Создатель Mario?', 'Сигэру Миямото', 'Хидэо Кодзима', 'Сид Мейер', 'Гейб Ньюэлл'),
            ('Первая игра в Zelda?', '1986', '1987', '1985', '1984')
        ]
        cursor.executemany('INSERT INTO question VALUES (NULL,?,?,?,?,?)', questions)
        
        quizes = [
            (1, 'История игр'),
            (2, 'Игровые персонажи')
        ]
        cursor.executemany('INSERT INTO quiz VALUES (?,?)', quizes)
        
        links = [
            (1, 1), (1, 2),
            (2, 3), (2, 4) 
        ]
        cursor.executemany('INSERT INTO quiz_content VALUES (NULL,?,?)', links)
        
        conn.commit()

if __name__ == '__main__':
    init_db()
    print("База данных инициализирована!")
