from fastapi import APIRouter, HTTPException
from app.database import vitals_collection, patients_collection
from app.models.vital import VitalModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/vitals", tags=["Vitals"])

def calculate_bmi(weight: float, height: float) -> float:
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def check_risk(vitals: dict) -> dict:
    flags = []
    risk_level = "Normal"

    # Blood pressure check
    bp = vitals.get("blood_pressure", "")
    if bp:
        systolic = int(bp.split("/")[0])
        if systolic >= 140:
            flags.append("⚠️ High Blood Pressure")
            risk_level = "High"
        elif systolic >= 120:
            flags.append("⚠️ Pre-Hypertension")
            risk_level = "Medium"

    # Blood sugar check
    sugar = vitals.get("blood_sugar", 0)
    if sugar >= 200:
        flags.append("⚠️ High Blood Sugar - Possible Diabetes")
        risk_level = "High"
    elif sugar >= 140:
        flags.append("⚠️ Pre-Diabetic Range")
        if risk_level != "High":
            risk_level = "Medium"

    # Hemoglobin check
    hb = vitals.get("hemoglobin", 0)
    if hb and hb < 8:
        flags.append("⚠️ Severe Anemia")
        risk_level = "High"
    elif hb and hb < 12:
        flags.append("⚠️ Mild Anemia")
        if risk_level == "Normal":
            risk_level = "Medium"

    # BMI check
    bmi = vitals.get("bmi", 0)
    if bmi >= 30:
        flags.append("⚠️ Obese")
    elif bmi < 18.5:
        flags.append("⚠️ Underweight")

    return {"risk_level": risk_level, "flags": flags}

# Record vitals
@router.post("/")
def record_vitals(vital: VitalModel):
    # Check patient exists
    patient = patients_collection.find_one(
        {"_id": ObjectId(vital.patient_id)}
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    vital_dict = vital.dict()

    # Auto calculate BMI
    vital_dict["bmi"] = calculate_bmi(vital.weight, vital.height)

    # Auto risk flagging
    risk = check_risk(vital_dict)
    vital_dict["risk_level"] = risk["risk_level"]
    vital_dict["risk_flags"] = risk["flags"]
    vital_dict["recorded_at"] = datetime.utcnow()

    result = vitals_collection.insert_one(vital_dict)
    return {
        "message": "Vitals recorded!",
        "bmi": vital_dict["bmi"],
        "risk_level": risk["risk_level"],
        "risk_flags": risk["flags"],
        "vital_id": str(result.inserted_id)
    }

# Get vitals by patient
@router.get("/{patient_id}")
def get_vitals(patient_id: str):
    vitals = []
    for v in vitals_collection.find({"patient_id": patient_id}):
        v["_id"] = str(v["_id"])
        vitals.append(v)
    return vitals

# Get all high risk patients in a camp
@router.get("/risk/{camp_id}")
def get_high_risk(camp_id: str):
    high_risk = []
    for v in vitals_collection.find({
        "camp_id": camp_id,
        "risk_level": {"$in": ["High", "Medium"]}
    }):
        v["_id"] = str(v["_id"])
        high_risk.append(v)
    return high_risk

@router.get("/all")
def get_all_vitals():
    vitals = []
    for v in vitals_collection.find():
        v["_id"] = str(v["_id"])
        vitals.append(v)
    return vitals