from fastapi import Depends, HTTPException
from starlette import status

from app.dependencies.dependencies import get_image_category_service
from app.services.image_category_service import ImageCategoryService


class ImageCategoryController:
    def __init__(self, image_category_service: ImageCategoryService = Depends(get_image_category_service)):
        self.image_category_service = image_category_service

    def get_all_categories(self):
        try:
            return self.image_category_service.get_all_categories()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al obtener categorias",
                "error": str(e)
            })
