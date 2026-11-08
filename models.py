from sqlalchemy import Column, Integer, String, Text
from database import Base


# ==========================================
# QUESTION TABLE
# ==========================================

class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    correct_answer = Column(
        Text,
        nullable=False
    )


# ==========================================
# STUDENT TABLE
# ==========================================

class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )


# ==========================================
# STUDENT ANSWERS TABLE
# ==========================================

class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        String(100),
        nullable=False
    )

    question_id = Column(
        Integer,
        nullable=False
    )

    student_answer = Column(
        Text,
        nullable=False
    )

    score = Column(
        Integer,
        default=0
    )