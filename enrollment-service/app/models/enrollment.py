from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # FK to students table
    course_id = Column(Integer, nullable=False)   # FK to courses table
    enrolled_at = Column(DateTime, default=datetime.utcnow)
