import os
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus
import logging

logging.basicConfig(level=logging.DEBUG)

# Enable HTTPConnection debug logging
import http.client
http.client.HTTPConnection.debuglevel = 1

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
def create_student(name: str = Form(...), email: str = Form(...)):
    # Internal call uses query parameters
    url = f"http://{STUDENT_SERVICE}/students/?name={quote_plus(name)}&email={quote_plus(email)}"
    requests.post(url)
    return RedirectResponse("/", status_code=303)


@app.post("/students/delete")
def delete_student(student_id: int = Form(...)):
    requests.delete(f"http://{STUDENT_SERVICE}/students/{student_id}")
    return RedirectResponse("/", status_code=303)


@app.post("/courses/create")
def create_course(title: str = Form(...), description: str = Form("")):
    url = f"http://{COURSE_SERVICE}/courses/?title={quote_plus(title)}&description={quote_plus(description)}"
    requests.post(url)
    return RedirectResponse("/", status_code=303)


@app.post("/courses/delete")
def delete_course(course_id: int = Form(...)):
    requests.delete(f"http://{COURSE_SERVICE}/courses/{course_id}")
    return RedirectResponse("/", status_code=303)


@app.post("/enrollments/create")
def create_enrollment(student_id: int = Form(...), course_id: int = Form(...)):
    url = f"http://{ENROLLMENT_SERVICE}/enrollments/?student_id={student_id}&course_id={course_id}"
    requests.post(url)
    return RedirectResponse("/", status_code=303)
