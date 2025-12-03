from fastapi import FastAPI
from app.database import Base, engine
from app.routers.course import router as course_router

app = FastAPI(title="Course Service")

Base.metadata.create_all(bind=engine)

app.include_router(course_router)

@app.get("/")
def root():
    return {"service": "course-service", "status": "running"}
