from pydantic import BaseModel, Field
from pydantic.schema import datetime

from app.schemas.tooth_schema import Tooth


class OdontogramBase(BaseModel):
    patient_id: int = Field(..., example=1)
    type_odontogram_id: int = Field(..., example=1)
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class OdontogramCreate(OdontogramBase):
    pass


class Odontogram(OdontogramBase):
    odontogram_id: int = Field(..., example=1)
    details: list[Tooth]
