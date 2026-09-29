from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.services.student_service import create_student, list_students, get_student, update_student, delete_student

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create(data: StudentCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Student).where(Student.email == data.email)):
        raise HTTPException(409, "A student with this email already exists")
    try: return create_student(db, data)
    except IntegrityError: db.rollback(); raise HTTPException(409, "Student could not be created")

@router.get("", response_model=list[StudentRead])
def read_all(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), department: str | None = None, course: str | None = None, db: Session = Depends(get_db)):
    return list_students(db, skip, limit, department, course)

@router.get("/{student_id}", response_model=StudentRead)
def read_one(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student: raise HTTPException(404, "Student not found")
    return student

@router.put("/{student_id}", response_model=StudentRead)
def update(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student: raise HTTPException(404, "Student not found")
    if data.email and db.scalar(select(Student).where(Student.email == data.email, Student.id != student_id)):
        raise HTTPException(409, "A student with this email already exists")
    return update_student(db, student, data)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student: raise HTTPException(404, "Student not found")
    delete_student(db, student)
