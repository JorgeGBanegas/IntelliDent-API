from fastapi import Depends, HTTPException
from starlette import status

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.dependencies.dependencies import get_odontogram_service
from app.services.odontogram_service import OdontogramService


class OdontogramController:
    def __init__(self, odontogram_service: OdontogramService = Depends(get_odontogram_service)):
        self.odontogram_service = odontogram_service

    def get_odontogram_by_id(self, odontogram_id: int):
        try:
            return self.odontogram_service.get_odontogram_by_id(odontogram_id)
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "message": "Odontograma no encontrado",
                                    "error": str(e)
                                })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener odontograma",
                                    "error": str(e)
                                })

    def get_odontogram_by_patient_id(self, patient_id: int):
        try:
            return self.odontogram_service.get_odontogram_by_patient_id(patient_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener odontograma",
                                    "error": str(e)
                                })

    def create_odontogram(self, odontogram):
        try:
            return self.odontogram_service.create_odontogram(odontogram)
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "message": "Error al crear odontograma",
                                    "error": str(e)
                                })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al crear odontograma",
                                    "error": str(e)
                                })

    def get_detail_odontogram(self, odontogram_id: int, tooth_number: int, page: int, limit: int):
        try:
            return self.odontogram_service.get_detail_odontogram(odontogram_id, tooth_number, page, limit)
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "message": "Error al obtener detalle de odontograma",
                                    "error": str(e)
                                })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al obtener detalle de odontograma",
                                    "error": str(e)
                                })

    def create_detail_odontogram(self, detail_odontogram):
        try:
            return self.odontogram_service.create_detail_odontogram(detail_odontogram)
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "message": "Error al crear detalle de odontograma",
                                    "error": str(e)
                                })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={
                                    "message": "Error al crear detalle de odontograma",
                                    "error": str(e)
                                })