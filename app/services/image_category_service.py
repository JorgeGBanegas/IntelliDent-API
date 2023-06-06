from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.models import ImageCategory
from app.schemas.image_category_schema import ImageCategory as ImageCategorySchema


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

    def get_all_categories(self):
        try:
            categories = self.db.query(ImageCategory).all()
            print(categories)
            categories_list = [ImageCategorySchema(image_category_id=category.image_category_id,
                                                   image_category_name=category.image_category_name)
                               for category in categories]
            return categories_list
        except Exception as e:
            raise ValueError(f"Error al obtener categoría: {e}")
