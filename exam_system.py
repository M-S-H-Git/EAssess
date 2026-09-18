import sqlite3
import csv
import datetime
import hashlib

# Database Initialization - FINAL CORRECTED SYNTAX
def init_db():
    conn = sqlite3.connect('exam_system.db')
    c = conn.cursor()
    
    # Users Table - CORRECTED
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT UNIQUE,
                 password TEXT,
                 role TEXT CHECK(role IN ('admin', 'teacher', 'student'))
              )''')
    
    # Questions Table - CORRECTED
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
    
    # Exams Table - CORRECTED
    c.execute('''CREATE TABLE IF NOT EXISTS exams (
                 id INTEGER PRIMARY KEY,
                 title TEXT,
                 exam_date TEXT,
                 duration INTEGER,
                 status TEXT DEFAULT 'New')
              ''')
    
    # Exam Questions Junction - CORRECTED
    c.execute('''CREATE TABLE IF NOT EXISTS exam_questions (
                 exam_id INTEGER,
                 question_id INTEGER,
                 FOREIGN KEY(exam_id) REFERENCES exams(id),
                 FOREIGN KEY(question_id) REFERENCES questions(id))
              ''')
    
    # Student Exams - CORRECTED
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
    
    # Student Answers - CORRECTED
    c.execute('''CREATE TABLE IF NOT EXISTS student_answers (
                 attempt_id INTEGER,
                 question_id INTEGER,
                 answer TEXT,
                 is_correct INTEGER,
                 FOREIGN KEY(attempt_id) REFERENCES student_exams(id))
              ''')
    
    conn.commit()
    return conn

# User Management
def register_user(conn, username, password, role):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                    (username, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate(conn, username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", 
                         (username, hashed))
    return cursor.fetchone()

# Question Bank Management
def add_question(conn, question_data):
    conn.execute('''INSERT INTO questions (
                 question_text, qtype, subject, difficulty, 
                 option_a, option_b, option_c, option_d, correct_answer)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', question_data)
    conn.commit()

def import_questions_from_csv(conn, filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_question(conn, (
                row['question_text'],
                row['qtype'],
                row['subject'],
                row['difficulty'],
                row.get('option_a', ''),
                row.get('option_b', ''),
                row.get('option_c', ''),
                row.get('option_d', ''),
                row['correct_answer']
            ))

# Exam Management
def create_exam(conn, title, exam_date, duration):
    conn.execute("INSERT INTO exams (title, exam_date, duration) VALUES (?, ?, ?)",
                (title, exam_date, duration))
    conn.commit()
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_question_to_exam(conn, exam_id, question_id):
    conn.execute("INSERT INTO exam_questions (exam_id, question_id) VALUES (?, ?)",
                (exam_id, question_id))
    conn.commit()

# Student Exam Interface
def start_exam(conn, student_id, exam_id):
    start_time = datetime.datetime.now().isoformat()
    conn.execute('''INSERT INTO student_exams (student_id, exam_id, start_time)
                 VALUES (?, ?, ?)''', (student_id, exam_id, start_time))
    conn.commit()
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]

def submit_answer(conn, attempt_id, question_id, answer, is_correct):
    conn.execute('''INSERT INTO student_answers (attempt_id, question_id, answer, is_correct)
                 VALUES (?, ?, ?, ?)''', (attempt_id, question_id, answer, int(is_correct)))
    conn.commit()

def finalize_exam(conn, attempt_id, score):
    end_time = datetime.datetime.now().isoformat()
    conn.execute('''UPDATE student_exams SET end_time = ?, score = ?
                 WHERE id = ?''', (end_time, score, attempt_id))
    conn.commit()

# Evaluation System
def evaluate_mcq(student_answer, correct_answer):
    return student_answer.strip().lower() == correct_answer.strip().lower()

def calculate_score(conn, attempt_id):
    cursor = conn.execute('''SELECT SUM(is_correct) FROM student_answers
                          WHERE attempt_id = ?''', (attempt_id,))
    return cursor.fetchone()[0] or 0

# Reporting
def generate_report(conn, exam_id):
    cursor = conn.execute('''SELECT u.username, se.score 
                          FROM student_exams se
                          JOIN users u ON se.student_id = u.id
                          WHERE se.exam_id = ?''', (exam_id,))
    return cursor.fetchall()

# Main Application
def main():
    import os
    if not os.path.exists('exam_system.db'):
        init_db()
    
with sqlite3.connect('exam_system.db') as conn:
    # Setup initial admin
    register_user(conn, "admin", "securepassword", "admin")
    
    while True:
        print("\nOnline Examination System")
        print("1. Login")
        print("2. Exit")
        choice = input("Select option: ")
        
        if choice == "2":
            break
        
        elif choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user = authenticate(conn, username, password)
            
            if not user:
                print("Invalid credentials")
                continue  # Return to the main menu
            
            user_id, role = user
            print(f"Logged in as {role.capitalize()}")

            # Admin Interface
            if role == "admin":
                while True:
                    print("\nAdmin Panel")
                    print("1. Add Question")
                    print("2. Create Exam")
                    print("3. Generate Report")
                    print("4. Logout")
                    admin_choice = input("Select option: ")
                    
                    if admin_choice == "4":
                        break
                        
                    # Add Question
                    elif admin_choice == "1":
                        qdata = (
                            input("Question: "),
                            input("Type (mcq/fill_blank/text): "),
                            input("Subject: "),
                            input("Difficulty: "),
                            input("Option A (if applicable): "),
                            input("Option B: "),
                            input("Option C: "),
                            input("Option D: "),
                            input("Correct Answer: ")
                        )
                        add_question(conn, qdata)
                        print("Question added!")
                    
                    # Create Exam
                    elif admin_choice == "2":
                        title = input("Exam Title: ")
                        date = input("Date (YYYY-MM-DD): ")
                        duration = int(input("Duration (minutes): "))
                        exam_id = create_exam(conn, title, date, duration)
                        
                        # Add questions to exam
                        while True:
                            qid = input("Add question ID (0 to finish): ")
                            if qid == "0": break
                            add_question_to_exam(conn, exam_id, int(qid))
                        print("Exam created!")
                    
                    # Reporting
                    elif admin_choice == "3":
                        exam_id = input("Enter Exam ID: ")
                        report = generate_report(conn, int(exam_id))
                        for row in report:
                            print(f"Student: {row[0]}, Score: {row[1]}")

            # Student Interface
            elif role == "student":
                print("\nAvailable Exams:")
                cursor = conn.execute("SELECT id, title FROM exams")
                for exam in cursor.fetchall():
                    print(f"{exam[0]}. {exam[1]}")
                
                exam_id = int(input("Select exam ID: "))
                attempt_id = start_exam(conn, user_id, exam_id)
                
                # Get exam questions
                cursor = conn.execute('''SELECT q.id, q.question_text, q.qtype, 
                                      q.option_a, q.option_b, q.option_c, q.option_d
                                      FROM questions q
                                      JOIN exam_questions eq ON q.id = eq.question_id
                                      WHERE eq.exam_id = ?''', (exam_id,))
                questions = cursor.fetchall()
                score = 0
                
                # Answer questions
                for q in questions:
                    qid, text, qtype, *options = q
                    print(f"\nQ: {text}")
                    
                    if qtype == "mcq":
                        for i, opt in enumerate(options, 65):  # ASCII 65 = 'A'
                            if opt: print(f"{chr(i)}. {opt}")
                        ans = input("Your answer (A-D): ").upper()
                    else:
                        ans = input("Your answer: ")
                    
                    # Check answer (MCQ only for auto-eval)
                    is_correct = 0
                    if qtype == "mcq":
                        cursor = conn.execute("SELECT correct_answer FROM questions WHERE id = ?", (qid,))
                        correct = cursor.fetchone()
                        if correct:
                            correct = correct[0]
                            is_correct = 1 if ans == correct else 0
                            if is_correct: 
                                print("✓ Correct!")
                                score += 1
                            else: 
                                print("✗ Incorrect!")
                    
                    submit_answer(conn, attempt_id, qid, ans, is_correct)
                
                # Finalize exam
                finalize_exam(conn, attempt_id, score)
                print(f"Exam completed! Your score: {score}/{len(questions)}")
                print("Thank you for completing the exam!")

if __name__ == "__main__":
    main()