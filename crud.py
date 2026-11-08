from sqlalchemy.orm import Session

from models import (
    Question,
    Student,
    StudentAnswer
)


# ==================================================
# CREATE QUESTION
# ==================================================

def create_question(
    db: Session,
    question: str,
    correct_answer: str
):

    new_question = Question(
        question=question,
        correct_answer=correct_answer
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


# ==================================================
# GET QUESTIONS
# ==================================================

def get_questions(db: Session):

    return db.query(Question).all()


# ==================================================
# STUDENT LOGIN
# ==================================================

def student_login(
    db: Session,
    student_id: str,
    name: str
):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    # Student already exists
    if student:

        # Update name if changed
        student.name = name

        db.commit()
        db.refresh(student)

        return student

    # Create new student
    new_student = Student(
        student_id=student_id,
        name=name
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ==================================================
# ANSWER CHECKING
# ==================================================

def check_answer(
    correct_answer: str,
    student_answer: str
):

    # Convert everything to lowercase
    correct_answer = correct_answer.lower().strip()
    student_answer = student_answer.lower().strip()

    # Empty answer
    if not student_answer:
        return 0

    # Exact match
    if correct_answer == student_answer:
        return 1

    # Split into words
    correct_words = set(correct_answer.split())
    student_words = set(student_answer.split())

    if len(correct_words) == 0:
        return 0

    # Find matching words
    matched_words = correct_words.intersection(
        student_words
    )

    percentage = (
        len(matched_words)
        / len(correct_words)
    ) * 100

    # 50% or more = 1 mark
    if percentage >= 50:
        return 1

    return 0


# ==================================================
# SAVE STUDENT ANSWER
# ==================================================

def save_answer(
    db: Session,
    student_id: str,
    question_id: int,
    student_answer: str
):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if question is None:
        return None

    score = check_answer(
        question.correct_answer,
        student_answer
    )

    # Check whether this student already
    # answered this question
    old_answer = db.query(StudentAnswer).filter(
        StudentAnswer.student_id == student_id,
        StudentAnswer.question_id == question_id
    ).first()

    if old_answer:

        old_answer.student_answer = student_answer
        old_answer.score = score

        db.commit()
        db.refresh(old_answer)

        return old_answer

    # New answer
    new_answer = StudentAnswer(
        student_id=student_id,
        question_id=question_id,
        student_answer=student_answer,
        score=score
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer


# ==================================================
# STUDENT RESULT
# ==================================================

def get_student_result(
    db: Session,
    student_id: str
):

    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if student is None:
        return None

    total_questions = db.query(
        Question
    ).count()

    answers = db.query(
        StudentAnswer
    ).filter(
        StudentAnswer.student_id == student_id
    ).all()

    correct_answers = sum(
        answer.score
        for answer in answers
    )

    answered_questions = len(answers)

    percentage = 0

    if total_questions > 0:

        percentage = (
            correct_answers
            / total_questions
        ) * 100

    return {
        "student_id": student.student_id,
        "student_name": student.name,
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": correct_answers,
        "marks": f"{correct_answers}/{total_questions}",
        "percentage": round(percentage, 2)
    }