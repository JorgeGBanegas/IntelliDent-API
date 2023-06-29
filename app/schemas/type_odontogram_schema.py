from pydantic import BaseModel, Field


class TypeOdontogramBase(BaseModel):
    name_type: str = Field(..., min_length=3, max_length=50, example="Odontograma Pediatrico")

    class Config:
        orm_mode = True


class TypeOdontogramCreate(TypeOdontogramBase):
    pass


class TypeOdontogram(TypeOdontogramBase):
    type_odontogram_id: int = Field(..., example=1)
