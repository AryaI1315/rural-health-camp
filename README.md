# 🏥 Rural Health Camp Organizer

> A full-stack web application to manage rural health camps in Maharashtra, India.
> Built with Python + FastAPI + MongoDB Atlas + HTML/CSS/JS

---

## 📌 Project Overview

The **Rural Health Camp Organizer** helps NGOs, government bodies, and medical volunteers digitally manage rural health camps. It covers the full workflow — from registering camps and patients to recording vitals, auto-detecting health risks, and generating PDF reports.

---

## 🚀 Features

- ✅ **Camp Registration** — Create camps with location, date, doctors, and NGO info
- ✅ **Patient Enrollment** — Register patients linked to specific camps
- ✅ **Vitals Recording** — Record BP, blood sugar, hemoglobin, weight, height
- ✅ **Auto Risk Flagging** — Instantly detects High / Medium / Normal risk
- ✅ **BMI Calculator** — Auto-calculates BMI from weight and height
- ✅ **PDF Report Generator** — One-click downloadable report for NGOs
- ✅ **Role-Based Login** — Admin, Doctor, and Volunteer access
- ✅ **Interactive Dashboard** — Stats, recent camps table, sidebar navigation

---

## 🧱 Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.10+ + FastAPI  |
| Database   | MongoDB Atlas (Cloud)   |
| ODM        | PyMongo                 |
| Frontend   | HTML5 + Bootstrap 5 + JS|
| PDF        | ReportLab               |
| Server     | Uvicorn (ASGI)          |

---

## 📁 Project Structure

```
rural-health-camp/
│
├── .env                        # MongoDB connection string (secret)
│
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # MongoDB connection & collections
│   │
│   ├── models/
│   │   ├── camp.py             # Camp data model
│   │   ├── patient.py          # Patient data model
│   │   └── vital.py            # Vitals data model
│   │
│   └── routes/
│       ├── camps.py            # /camps API endpoints
│       ├── patients.py         # /patients API endpoints
│       ├── vitals.py           # /vitals API endpoints
│       └── reports.py          # /reports PDF generation
│
└── frontend/
    ├── login.html              # Login page (3 roles)
    └── dashboard.html          # Main app dashboard
```

---

## ⚙️ Setup & Installation

### 1. Clone the project
```bash
git clone https://github.com/yourusername/rural-health-camp.git
cd rural-health-camp
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn pymongo python-dotenv reportlab
```

### 4. Set up MongoDB Atlas
- Create a free account at [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
- Create a free M0 cluster (select Mumbai region)
- Create a database user and allow network access
- Copy your connection string

### 5. Create `.env` file
```
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/healthcamp
```

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

### 7. Open the frontend
- Open `frontend/login.html` in Chrome
- Login with demo credentials below

---

## 🔐 Login Credentials

| Role        | Username    | Password  |
|-------------|-------------|-----------|
| Admin / NGO | `admin`     | `admin123`|
| Doctor      | `doctor`    | `doc123`  |
| Volunteer   | `volunteer` | `vol123`  |

---

## 🌐 API Endpoints

| Method | Endpoint                        | Description                        |
|--------|---------------------------------|------------------------------------|
| POST   | `/camps/`                       | Create a new health camp           |
| GET    | `/camps/`                       | Get all camps                      |
| GET    | `/camps/{camp_id}`              | Get a single camp                  |
| POST   | `/patients/`                    | Register a patient                 |
| GET    | `/patients/camp/{camp_id}`      | Get all patients in a camp         |
| GET    | `/patients/{patient_id}`        | Get a single patient               |
| POST   | `/vitals/`                      | Record vitals + auto risk flagging |
| GET    | `/vitals/{patient_id}`          | Get patient vitals history         |
| GET    | `/vitals/risk/{camp_id}`        | Get high/medium risk patients      |
| GET    | `/reports/{camp_id}`            | Download PDF report                |

> 📖 Full interactive API docs available at: `http://127.0.0.1:8000/docs`

---

## 🧠 Auto Risk Flagging Logic

```
Blood Pressure >= 140  →  ⚠️ High BP           (High Risk)
Blood Pressure >= 120  →  ⚠️ Pre-Hypertension  (Medium Risk)
Blood Sugar    >= 200  →  ⚠️ Possible Diabetes  (High Risk)
Blood Sugar    >= 140  →  ⚠️ Pre-Diabetic       (Medium Risk)
Hemoglobin     <  8    →  ⚠️ Severe Anemia      (High Risk)
Hemoglobin     < 12    →  ⚠️ Mild Anemia        (Medium Risk)
BMI is auto-calculated from weight and height
```

---

## 🗃️ MongoDB Collections

| Collection  | Purpose                              |
|-------------|--------------------------------------|
| `camps`     | Health camp registrations            |
| `patients`  | Patient enrollments per camp         |
| `vitals`    | Vitals records with risk flags       |
| `followups` | Follow-up reminders for patients     |

---

## 📄 PDF Report Includes

- Camp name, date, village, district, NGO name, doctors
- Color-coded summary table (Red = High Risk, Yellow = Medium, Green = Normal)
- Full patient details table with vitals and risk flags
- Auto-generated timestamp

---

## 🔮 Future Scope

- [ ] Follow-up SMS reminders for patients
- [ ] MongoDB geo-queries to find camps within 50km
- [ ] Offline mode with local storage sync
- [ ] OTP-based real authentication
- [ ] Medicine inventory tracker
- [ ] District-wise data visualization charts
- [ ] React Native mobile app for field volunteers

---

## 💼 Interview Summary

> *"I built a full-stack health camp management system for rural Maharashtra using Python FastAPI as backend, MongoDB Atlas as database, and HTML/CSS/JS as frontend. The system allows NGOs to register camps, register patients, record vitals with automatic risk flagging for BP, diabetes, and anemia, and generate PDF reports. I used MongoDB's flexible document model for nested data like doctor arrays and medicine lists, and geospatial coordinates for camp locations."*

---

## 👩‍💻 Developer

**Arya** — 3rd Year Engineering Student  
Sangli, Maharashtra, India

---

## 📜 License

This project is built for educational purposes.
```
