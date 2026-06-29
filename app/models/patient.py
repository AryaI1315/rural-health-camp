from pydantic import BaseModel
from typing import Optional

class PatientModel(BaseModel):
    name: str
    age: int
    gender: str                      # Male / Female / Other
    village: str
    phone: str
    camp_id: str                     # which camp they registered in