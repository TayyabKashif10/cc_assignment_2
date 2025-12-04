from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.enrollment import Enrollment

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)

@router.post("/")
def create_enrollment(student_id: int, course_id: int, db: Session = Depends(get_db)):
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@router.get("/")
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()
