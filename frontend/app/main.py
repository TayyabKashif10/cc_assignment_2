import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Read service IPs from environment variables
COURSE_SERVICE = os.getenv("COURSE_SERVICE_IP")
STUDENT_SERVICE = os.getenv("STUDENT_SERVICE_IP")
ENROLLMENT_SERVICE = os.getenv("ENROLLMENT_SERVICE_IP")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Fetch students, courses, enrollments
    students = requests.get(f"http://{STUDENT_SERVICE}/students/").json()
    courses = requests.get(f"http://{COURSE_SERVICE}/courses/").json()
    enrollments = requests.get(f"http://{ENROLLMENT_SERVICE}/enrollments/").json()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "students": students, "courses": courses, "enrollments": enrollments}
    )

@app.post("/students/create")
def create_student(name: str, email: str):
    # Send as query parameters
    requests.post(f"http://{STUDENT_SERVICE}/students/", params={"name": name, "email": email})
    return RedirectResponse("/", status_code=303)

@app.post("/students/delete")
def delete_student(student_id: int):
    requests.delete(f"http://{STUDENT_SERVICE}/students/{student_id}")
    return RedirectResponse("/", status_code=303)

@app.post("/courses/create")
def create_course(title: str, description: str = ""):
    requests.post(f"http://{COURSE_SERVICE}/courses/", params={"title": title, "description": description})
    return RedirectResponse("/", status_code=303)

@app.post("/courses/delete")
def delete_course(course_id: int):
    requests.delete(f"http://{COURSE_SERVICE}/courses/{course_id}")
    return RedirectResponse("/", status_code=303)

@app.post("/enrollments/create")
def create_enrollment(student_id: int, course_id: int):
    requests.post(
        f"http://{ENROLLMENT_SERVICE}/enrollments/",
        params={"student_id": student_id, "course_id": course_id}
    )
    return RedirectResponse("/", status_code=303)
