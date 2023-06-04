from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.tooth_schema import Tooth


class Image(BaseModel):
    title: str
    image_base64: str
    teeth: list[int]


class DentalImageBase(BaseModel):
    patient_id: int
    image_category_id: int
    image_file: list[Image]
    created_at: datetime = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        validate_assignment = True


class DentalImage(DentalImageBase):
    dental_image_id: int


class DentalImageCreate(DentalImageBase):
    pass


class DentalImageItemList(BaseModel):
    dental_image_id: int
    path: str
    title: str

