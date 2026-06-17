from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
import models
from auth import create_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates") 
# ---------------- LOGIN ----------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    token = create_token({"user": email})
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("token", token)
    return response

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ---------------- PATIENT ----------------
@app.get("/patients", response_class=HTMLResponse)
def patients(request: Request):
    db = SessionLocal()
    data = db.query(models.Patient).all()
    return templates.TemplateResponse("patients.html", {"request": request, "patients": data})

@app.post("/patient/create")
def create_patient(name: str = Form(...), age: int = Form(...), phone: str = Form(...)):
    db = SessionLocal()
    db.add(models.Patient(name=name, age=age, phone=phone))
    db.commit()
    return RedirectResponse("/patients", 303)

# ---------------- DOCTOR ----------------
@app.get("/doctors", response_class=HTMLResponse)
def doctors(request: Request):
    db = SessionLocal()
    data = db.query(models.Doctor).all()
    return templates.TemplateResponse("doctors.html", {"request": request, "doctors": data})

@app.post("/doctor/create")
def create_doctor(name: str = Form(...), specialization: str = Form(...)):
    db = SessionLocal()
    db.add(models.Doctor(name=name, specialization=specialization))
    db.commit()
    return RedirectResponse("/doctors", 303)

# ---------------- APPOINTMENT ----------------
@app.get("/appointments", response_class=HTMLResponse)
def appointments(request: Request):
    db = SessionLocal()
    data = db.query(models.Appointment).all()
    return templates.TemplateResponse("appointments.html", {"request": request, "appointments": data})

@app.post("/appointment/create")
def create_appointment(
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
):
    db = SessionLocal()
    db.add(models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=date,
        time=time,
        status="Scheduled"
    ))
    db.commit()
    return RedirectResponse("/appointments", 303)