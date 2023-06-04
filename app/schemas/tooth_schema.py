from pydantic import BaseModel, Field


class ToothBase(BaseModel):
    tooth_name: str = Field(..., min_length=3, max_length=50, example="Incisivo")
    numeration: int = Field(..., ge=11, le=48, example=11)

    class Config:
        orm_mode = True
        validate_assignment = True


class Tooth(ToothBase):
    tooth_id: int = Field(..., example=1)
