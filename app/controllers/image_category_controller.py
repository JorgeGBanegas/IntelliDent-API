from fastapi import Depends

from app.dependencies.dependencies import get_image_category_service
from app.services.image_category_service import ImageCategoryService


class ImageCategoryController:
    def __init__(self, image_category_service: ImageCategoryService = Depends(get_image_category_service)):
        self.image_category_service = image_category_service

    def get_all_categories(self):
        try:
            return self.image_category_service.get_all_categories()
        except Exception as e:
            raise ValueError(f"Error al obtener categorías: {e}")
