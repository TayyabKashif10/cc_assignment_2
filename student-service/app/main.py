from fastapi import FastAPI
from app.database import Base, engine
from app.routers.student import router as student_router

app = FastAPI(title="Student Service")

# Create tables on startup if they don't exist (simple approach for now)
Base.metadata.create_all(bind=engine)

app.include_router(student_router)

@app.get("/")
def root():
    return {"service": "student-service", "status": "running"}
