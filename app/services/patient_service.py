from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate
import logging

# configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def add_patient(self, patient: PatientCreate, user_id) -> Patient:
        try:
            patient = Patient(**patient.dict())
            patient.created_by = user_id
            self.db.add(patient)
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except Exception as e:
            self.logger.error(f"Error al agregar paciente: {e}")
            raise ValueError(f"Error al agregar paciente a la base de datos : {e}")


