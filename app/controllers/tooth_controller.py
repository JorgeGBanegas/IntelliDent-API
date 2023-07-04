from fastapi import Depends, HTTPException
from starlette import status

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.dependencies.dependencies import get_tooth_service
from app.services.tooth_service import ToothService


class ToothController:
    def __init__(self, tooth_service: ToothService = Depends(get_tooth_service)):
        self.tooth_service = tooth_service

    def get_all_teeth(self):
        try:
            return self.tooth_service.get_all_teeth()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener dientes",
                                    "error": str(e)
                                })

    def get_tooth_by_number(self, tooth_number: int):
        try:
            return self.tooth_service.get_tooth_by_number(tooth_number)
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "message": "Diente no encontrado",
                                    "error": str(e)
                                })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener diente",
                                    "error": str(e)
                                })