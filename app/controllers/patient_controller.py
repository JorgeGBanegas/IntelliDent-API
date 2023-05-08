import logging
from fastapi import HTTPException, Depends
from starlette import status
from app.dependencies.dependencies import get_patient_service
from app.services.patient_service import PatientService

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class PatientController:
    def __init__(self, patient_service: PatientService = Depends(get_patient_service)):
        self.patient_service = patient_service
        self.logger = logging.getLogger(__name__)

    def add_patient(self, patient,  user_id):
        try:
            return self.patient_service.add_patient(patient, user_id)
        except Exception as e:
            self.logger.error(f"Error al agregar paciente {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al agregar paciente",
                "error": str(e)
            })
