from fastapi import Depends

from app.dependencies.dependencies import get_treatment_service
from app.services.treatment_service import TreatmentService


class TreatmentController:
    def __init__(self, tratment_service: TreatmentService = Depends(get_treatment_service)):
        self.treatment_service = tratment_service

    def get_all_treatments(self, search):
        try:
            return self.treatment_service.get_all_treatments(search)
        except Exception as e:
            raise ValueError(f"Error al obtener tratamientos de la base de datos : {e}")

    def add_treatment(self, treatment):
        try:
            return self.treatment_service.add_treatment(treatment)
        except Exception as e:
            raise ValueError(f"Error al guardar tratamiento en la base de datos : {e}")
