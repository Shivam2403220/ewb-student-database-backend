from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def create_student(db: Session, data: StudentCreate):
    student = Student(**data.model_dump())
    db.add(student); db.commit(); db.refresh(student)
    return student

def list_students(db: Session, skip=0, limit=100, department=None, course=None):
    stmt = select(Student).offset(skip).limit(limit)
    if department: stmt = stmt.where(Student.department.ilike(department))
    if course: stmt = stmt.where(Student.course.ilike(course))
    return list(db.scalars(stmt).all())

def get_student(db: Session, student_id: int):
    return db.get(Student, student_id)

def update_student(db: Session, student: Student, data: StudentUpdate):
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(student, key, value)
    db.commit(); db.refresh(student)
    return student

def delete_student(db: Session, student: Student):
    db.delete(student); db.commit()
