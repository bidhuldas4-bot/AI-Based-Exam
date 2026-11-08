from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Question, Student

from crud import (
    create_question,
    get_questions,
    student_login,
    save_answer,
    get_student_result
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Online Exam Application",
    description="Teacher and Student Examination System",
    version="1.0"
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# PYDANTIC MODELS
# =========================================================

class QuestionCreate(BaseModel):
    question: str
    correct_answer: str


class StudentLogin(BaseModel):
    student_id: str
    name: str


class StudentAnswerCreate(BaseModel):
    student_id: str
    question_id: int
    student_answer: str


# =========================================================
# 1. TEACHER - ADD QUESTION
# =========================================================

@app.post("/teacher/questions")
def add_question(
    data: QuestionCreate,
    db: Session = Depends(get_db)
):

    if not data.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if not data.correct_answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Correct answer cannot be empty"
        )

    question = create_question(
        db,
        data.question.strip(),
        data.correct_answer.strip()
    )

    return {
        "message": "Question added successfully",
        "id": question.id,
        "question": question.question
    }


# =========================================================
# 2. GET EXAM QUESTIONS
#
# IMPORTANT:
# correct_answer is NOT returned to the student.
# =========================================================

@app.get("/exam/questions")
def exam_questions(
    db: Session = Depends(get_db)
):

    questions = get_questions(db)

    return {
        "total_questions": len(questions),
        "questions": [
            {
                "id": question.id,
                "question": question.question
            }
            for question in questions
        ]
    }


# =========================================================
# 3. STUDENT LOGIN
# =========================================================

@app.post("/student/login")
def login_student(
    data: StudentLogin,
    db: Session = Depends(get_db)
):

    if not data.student_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Student ID is required"
        )

    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Student name is required"
        )

    student = student_login(
        db,
        data.student_id.strip(),
        data.name.strip()
    )

    return {
        "message": "Login successful",
        "student_id": student.student_id,
        "name": student.name
    }


# =========================================================
# 4. SUBMIT STUDENT ANSWER
# =========================================================

@app.post("/exam/answer")
def submit_answer(
    data: StudentAnswerCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.student_id == data.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    answer = save_answer(
        db,
        data.student_id,
        data.question_id,
        data.student_answer
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return {
        "message": "Answer saved successfully",
        "question_id": data.question_id
    }


# =========================================================
# 5. STUDENT RESULT
# =========================================================

@app.get("/result/{student_id}")
def student_result(
    student_id: str,
    db: Session = Depends(get_db)
):

    result = get_student_result(
        db,
        student_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return result


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def home():
    return FileResponse(
        "static/index.html"
    )


# =========================================================
# TEACHER PAGE
# =========================================================

@app.get("/teacher")
def teacher_page():
    return FileResponse(
        "static/teacher.html"
    )


# =========================================================
# STUDENT LOGIN PAGE
# =========================================================

@app.get("/login")
def login_page():
    return FileResponse(
        "static/login.html"
    )


# =========================================================
# EXAM PAGE
# =========================================================

@app.get("/exam")
def exam_page():
    return FileResponse(
        "static/exam.html"
    )


# =========================================================
# RESULT PAGE
# =========================================================

@app.get("/result")
def result_page():
    return FileResponse(
        "static/result.html"
    )