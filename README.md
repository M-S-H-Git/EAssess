# EAssess: Online Examination System

EAssess is a Python and SQLite prototype for a secure, scalable online examination platform. It is based on the accompanying Software Requirements Specification (SRS) for the Sindh Board of Education (SBoE) examination workflow.

The SRS defines the broader target system, including a web interface, role-based access control, question-bank management, scheduled exams, student registration, grading, reporting, and SBoE API integration. The code in this repository is a command-line proof of concept for the core data and examination workflows.

## Current Prototype Features

- SQLite database initialization for users, questions, exams, exam questions, student attempts, and answers
- User registration and authentication for `admin`, `teacher`, and `student` roles
- SHA-256 password hashing for the educational prototype
- Question-bank entry with MCQ, fill-in-the-blank, and text question types
- CSV question import support
- Exam creation, scheduling fields, duration, and question association
- Student exam attempts and answer recording
- Automatic MCQ evaluation and score calculation
- Exam completion timestamps and score storage
- Basic report generation showing student scores by exam

## SRS Scope

The full SRS specifies the following intended platform capabilities:

- Secure authentication and role-based authorization
- Question creation, editing, deletion, categorization, and Excel import
- Exam creation, scheduling, randomization, timing, and status tracking
- Student registration, payment, system checks, exam delivery, and result viewing
- Automated and subjective evaluation
- SBoE API result posting with timeouts and acknowledgements
- Performance reporting and analytics with PDF/Excel export
- Responsive web access, HTTPS, encryption, 99.9% availability, and support for up to 1,000 concurrent users

The diagrams and workflow requirements are documented in [EAssess_SRS.pdf](EAssess_SRS.pdf).

## Requirements

- Python 3.8 or newer
- SQLite, included with Python
- No third-party Python packages are required

## Run The Prototype

Run commands from the project directory.

Initialize the database and create the demonstration administrator:

```bash
python create_db.py
```

Start the command-line examination system:

```bash
python exam_system.py
```

The default demonstration administrator is:

```text
Username: admin
Password: securepassword
```

The application creates `exam_system.db` in the current directory. This generated database is excluded from version control.

## Main Workflow

### Administrator

1. Log in with the administrator account.
2. Add questions and their answer choices.
3. Create an exam with a date and duration.
4. Associate question IDs with the exam.
5. Generate a basic score report.

### Student

1. Register a student account in the database layer.
2. Log in.
3. Select an available exam.
4. Answer the displayed questions.
5. Submit the attempt and view the calculated score.

## Project Structure

```text
.
|-- create_db.py       Database schema and initial administrator setup
|-- exam_system.py     Authentication, question, exam, grading, and reporting prototype
|-- EAssess_SRS.pdf    Software Requirements Specification
`-- README.md
```

## Security And Production Notes

This repository is an educational prototype and is not production-ready. For deployment, replace direct SHA-256 password hashing with a password-hashing scheme such as Argon2id or bcrypt, add secure session management, validate all input, enforce authorization at every operation, use parameterized database access consistently, protect secrets, enable HTTPS, and add audit logging.

The web frontend, payment workflow, SBoE API integration, subjective grading, concurrency testing, encrypted storage, backup/recovery, and production availability requirements from the SRS are not implemented in this command-line prototype.

## Report

See [EAssess_SRS.pdf](EAssess_SRS.pdf) for the full Software Requirements Specification, functional and non-functional requirements, wireframes, use cases, activity diagrams, development iterations, issue list, and glossary.

## Author

Muhammed Salah Hussain  
GitHub: [M-S-H-Git](https://github.com/M-S-H-Git)  
LinkedIn: [Muhammed Salah Hussain](https://linkedin.com/in/muhammed-salah-hussain-231797388)
