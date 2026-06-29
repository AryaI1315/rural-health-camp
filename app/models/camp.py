from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    latitude: float
    longitude: float

class CampModel(BaseModel):
    camp_name: str
    date: str                        # format: "2024-03-15"
    village: str
    district: str
    state: str = "Maharashtra"
    organized_by: str
    doctors: List[str]
    location: Location
    status: str = "upcoming"         # upcoming / ongoing / completed