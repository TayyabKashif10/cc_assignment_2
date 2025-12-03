from fastapi import FastAPI
from app.database import Base, engine
from app.routers.enrollment import router as enrollment_router

app = FastAPI(title="Enrollment Service")

Base.metadata.create_all(bind=engine)

app.include_router(enrollment_router)

@app.get("/")
def root():
    return {"service": "enrollment-service", "status": "running"}
