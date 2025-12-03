from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/")
def create_student(name: str, email: str, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    student = Student(name=name, email=email)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/")
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"status": "deleted"}
