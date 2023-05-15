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

    def add_patient(self, patient, user_id):
        try:
            return self.patient_service.add_patient(patient, user_id)
        except Exception as e:
            self.logger.error(f"Error al agregar paciente {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al agregar paciente",
                "error": str(e)
            })

    def get_all_patients(self, search_query, page, limit):
        try:
            return self.patient_service.get_all_patients(search_query, page, limit)
        except Exception as e:
            self.logger.error(f"Error al obtener pacientes {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al obtener pacientes",
                "error": str(e)
            })

    def get_patient_by_id(self, patient_id):
        try:
            patient = self.patient_service.get_patient_by_id(patient_id)
            if not patient:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                    "message": "Paciente no encontrado",
                    "error": "No se encontró un paciente con el id especificado"
                })
            return patient
        except HTTPException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error al obtener paciente {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al obtener paciente",
                "error": str(e)
            })

    def update_patient(self, patient_id, patient_update):
        try:
            patient = self.patient_service.update_patient(patient_id, patient_update)
            return patient
        except FileNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "Paciente no encontrado",
                "error": str(e)
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al actualizar paciente",
                "error": str(e)
            })