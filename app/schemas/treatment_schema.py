from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TreatmentBase(BaseModel):
    name_treatment: str = Field(..., min_length=3, max_length=50, example="Limpieza")
    description: Optional[str] = None
    created_at: datetime = None
    deleted_at: datetime = None

    class Config:
        orm_mode = True


class TreatmentCreate(TreatmentBase):
    pass


class Treatment(TreatmentBase):
    treatment_id: int = Field(..., example=1)
