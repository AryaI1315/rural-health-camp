from fastapi import FastAPI
from app.routes import camps, patients, vitals, reports

app = FastAPI(title="Rural Health Camp Organizer 🏥")

app.include_router(camps.router)
app.include_router(patients.router)
app.include_router(vitals.router)
app.include_router(reports.router)

@app.get("/")
def home():
    return {"message": "Rural Health Camp API is running! 🏥"}