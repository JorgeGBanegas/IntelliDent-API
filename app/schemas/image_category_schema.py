from typing import Optional

from pydantic import Field, BaseModel


class ImageCategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="Radiografía")
    description: Optional[str] = None

    class Config:
        orm_mode = True
        validate_assignment = True


class ImageCategory(ImageCategoryBase):
    image_category_id: int = Field(..., example=1)
