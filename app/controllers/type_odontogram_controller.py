from fastapi import Depends, HTTPException
from starlette import status

from app.dependencies.dependencies import get_type_odontogram_service
from app.services.type_odontogram_service import TypeOdontogramService


class TypeOdontogramController:
    def __init__(self, type_odontogram_service: TypeOdontogramService = Depends(get_type_odontogram_service)):
        self.type_odontogram_service = type_odontogram_service

    def get_all_type_odontogram(self):
        try:
            return self.type_odontogram_service.get_all_type_odontogram()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener tipos de odontograma",
                                    "error": str(e)
                                })

