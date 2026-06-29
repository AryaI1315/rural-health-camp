from fastapi import APIRouter, HTTPException
from app.database import camps_collection
from app.models.camp import CampModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/camps", tags=["Camps"])

# Create a new camp
@router.post("/")
def create_camp(camp: CampModel):
    camp_dict = camp.dict()
    camp_dict["created_at"] = datetime.utcnow()
    result = camps_collection.insert_one(camp_dict)
    return {"message": "Camp created!", "camp_id": str(result.inserted_id)}

# Get all camps
@router.get("/")
def get_all_camps():
    camps = []
    for camp in camps_collection.find():
        camp["_id"] = str(camp["_id"])
        camps.append(camp)
    return camps

# Get single camp
@router.get("/{camp_id}")
def get_camp(camp_id: str):
    camp = camps_collection.find_one({"_id": ObjectId(camp_id)})
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    camp["_id"] = str(camp["_id"])
    return camp