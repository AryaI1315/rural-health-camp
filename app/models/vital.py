from pydantic import BaseModel
from typing import List, Optional

class VitalModel(BaseModel):
    patient_id: str
    camp_id: str
    blood_pressure: str              # e.g. "130/85"
    blood_sugar: float               # mg/dL
    weight: float                    # kg
    height: float                    # cm
    hemoglobin: Optional[float]      # g/dL
    diagnosis: Optional[str]
    medicines_given: List[str] = []