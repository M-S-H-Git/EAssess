import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect('exam_system.db')
    c = conn.cursor()
    
    # Create Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             username TEXT UNIQUE,
             password TEXT,
             role TEXT CHECK(role IN ('admin', 'teacher', 'student'))
          )''')

    
    # Create Questions Table
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                 id INTEGER PRIMARY KEY,
                 question_text TEXT NOT NULL,
                 qtype TEXT CHECK(qtype IN ('mcq', 'fill_blank', 'text')),
                 subject TEXT,
                 difficulty TEXT,
                 option_a TEXT,
                 option_b TEXT,
                 option_c TEXT,
                 option_d TEXT,
                 correct_answer TEXT)
              ''')
    
    # Create Exams Table
    c.execute('''CREATE TABLE IF NOT EXISTS exams (
                 id INTEGER PRIMARY KEY,
                 title TEXT,
                 exam_date TEXT,
                 duration INTEGER,
                 status TEXT DEFAULT 'New')
              ''')
    
    # Create Exam Questions Junction Table
    c.execute('''CREATE TABLE IF NOT EXISTS exam_questions (
                 exam_id INTEGER,
                 question_id INTEGER,
                 FOREIGN KEY(exam_id) REFERENCES exams(id),
                 FOREIGN KEY(question_id) REFERENCES questions(id))
              ''')
    
    # Create Student Exams Table
    c.execute('''CREATE TABLE IF NOT EXISTS student_exams (
                 id INTEGER PRIMARY KEY,
                 student_id INTEGER,
                 exam_id INTEGER,
                 start_time TEXT,
                 end_time TEXT,
                 score REAL,
                 FOREIGN KEY(student_id) REFERENCES users(id),
                 FOREIGN KEY(exam_id) REFERENCES exams(id))
              ''')
    
    # Create Student Answers Table
    c.execute('''CREATE TABLE IF NOT EXISTS student_answers (
                 attempt_id INTEGER,
                 question_id INTEGER,
                 answer TEXT,
                 is_correct INTEGER,
                 FOREIGN KEY(attempt_id) REFERENCES student_exams(id))
              ''')
    
    # Create admin user
    hashed_password = hashlib.sha256("securepassword".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  ('admin', hashed_password, 'admin'))
    except sqlite3.IntegrityError:
        pass  # Admin already exists
    
    conn.commit()
    conn.close()
    print("Database 'exam_system.db' created successfully!")
    print("Admin credentials: username='admin', password='securepassword'")

if __name__ == '__main__':
    create_database()