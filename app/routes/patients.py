from fastapi import APIRouter, HTTPException
from app.database import patients_collection, camps_collection
from app.models.patient import PatientModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/patients", tags=["Patients"])

# Register a patient
@router.post("/")
def register_patient(patient: PatientModel):
    # Check if camp exists
    camp = camps_collection.find_one({"_id": ObjectId(patient.camp_id)})
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")

    patient_dict = patient.dict()

    # Auto-generate patient ID
    count = patients_collection.count_documents({})
    patient_dict["patient_id"] = f"RHC-2024-{count+1:03d}"
    patient_dict["registered_at"] = datetime.utcnow()

    result = patients_collection.insert_one(patient_dict)
    return {
        "message": "Patient registered!",
        "patient_id": patient_dict["patient_id"],
        "db_id": str(result.inserted_id)
    }

# Get all patients in a camp
@router.get("/camp/{camp_id}")
def get_patients_by_camp(camp_id: str):
    patients = []
    for p in patients_collection.find({"camp_id": camp_id}):
        p["_id"] = str(p["_id"])
        patients.append(p)
    return patients

# Get single patient
@router.get("/{patient_id}")
def get_patient(patient_id: str):
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient["_id"] = str(patient["_id"])
    return patient