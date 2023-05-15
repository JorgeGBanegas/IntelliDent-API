import logging
from fastapi import HTTPException, Depends
from starlette import status

from app.Exceptions.persistence_exceptions import RecordNotFoundException, RecordAlreadyExistsException, \
    IntegrityErrorException
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
        except RecordAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                "message": "El registro ya existe en la base de datos",
                "error": str(e)
            })
        except IntegrityErrorException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                "message": "Error de integridad en la base de datos",
                "error": str(e)
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al agregar paciente",
                "error": str(e)
            })

    def get_all_patients(self, search_query, page, limit):
        try:
            return self.patient_service.get_all_patients(search_query, page, limit)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al obtener pacientes",
                "error": str(e)
            })

    def get_patient_by_id(self, patient_id):
        try:
            patient = self.patient_service.get_patient_by_id(patient_id)
            return patient

        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "Paciente no encontrado",
                "error": str(e)
            })
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
        except RecordNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "Paciente no encontrado",
                "error": str(e)
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al actualizar paciente",
                "error": str(e)
            })
