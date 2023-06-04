from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.models.image_category import ImageCategory


class ImageCategoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_category_by_id(self, category_id: int):
        try:
            # obtener categoría con id
            category = self.db.query(ImageCategory).filter(ImageCategory.image_category_id == category_id).first()
            if category is None:
                raise RecordNotFoundException("No se encontró la categoría")
            return category

        except RecordNotFoundException:
            raise
        except Exception as e:
            raise ValueError(f"Error al obtener categoría: {e}")
