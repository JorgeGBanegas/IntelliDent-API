from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.tooth_schema import Tooth
from app.schemas.treatment_schema import Treatment


class DetailOdontogramBase(BaseModel):
    description: Optional[str] = None
    odontogram_id: int = Field(..., example=1)
    tooth_id: int = Field(..., example=1)
    treatment_id: int = Field(..., example=1)
    created_at: datetime = None

    class Config:
        orm_mode = True


class DetailOdontogramCreate(BaseModel):
    description: Optional[str] = None
    odontogram_id: int = Field(..., example=1)
    tooth_number: int = Field(..., example=1)
    treatment_id: int = Field(..., example=1)
    created_at: datetime = None


class DetailOdontogram(DetailOdontogramBase):
    detail_odontogram_id: int = Field(..., example=1)


class DetailOdontogramItem(BaseModel):
    detail_odontogram_id: int = Field(..., example=1)
    description: Optional[str] = None
    odontogram_id: int = Field(..., example=1)
    tooth: Tooth
    treatment: Treatment
    created_at: datetime

    class Config:
        orm_mode = True
