from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.dependencies.dependencies import get_dental_image_service
from app.services.dental_image_service import DentalImageService


class DentalImageController:
    def __init__(self, dental_image_service: DentalImageService = Depends(get_dental_image_service)):
        self.dental_image_service = dental_image_service

    def get_all_dental_images_by_patient_and_category(self, patient_id: int, category_id: int):
        try:
            return self.dental_image_service.get_all_dental_images_by_patient_and_category(patient_id, category_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al obtener imagenes",
                "error": str(e)
            })

    def save_dental_images(self, image_file):
        try:
            return self.dental_image_service.save_dental_images(image_file)

        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "message": "Error al guardar imagen",
                "error": str(e)
            })
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "Error al guardar imagen, Verifique los datos enviados",
                "error": str(e)
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al guardar imagen",
                "error": str(e)
            })