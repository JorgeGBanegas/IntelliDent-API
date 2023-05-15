from typing import List, Type

from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientUpdate
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

    # get al patients with pagination
    def get_all_patients(self, search_query, page, limit) -> List[Type[Patient]]:
        try:
            query = self.db.query(Patient)
            if search_query:
                query = query.filter(Patient.first_name.ilike(f"%{search_query}%") |
                                     Patient.last_name.ilike(f"%{search_query}%"))

            query = query.order_by(Patient.first_name)
            patients = query.offset(page * limit).limit(limit).all()
            return patients
        except Exception as e:
            self.logger.error(f"Error al obtener pacientes: {e}")
            raise ValueError(f"Error al obtener pacientes de la base de datos : {e}")

    # get patient by id
    def get_patient_by_id(self, patient_id) -> Patient:
        try:
            patient = self.db.query(Patient).get(patient_id)
            if not patient:
                raise FileNotFoundError(f"No se encontró un paciente con el id especificado")
            return patient
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error al obtener paciente de la base de datos : {e}")

    # update patient
    def update_patient(self, patient_id, patient_update: PatientUpdate) -> Patient:
        try:
            patient = self.db.query(Patient).get(patient_id)
            if not patient:
                raise FileNotFoundError(f"No se encontró un paciente con el id especificado")

            for var, value in vars(patient_update).items():
                if value is not None:
                    setattr(patient, var, value)
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error al actualizar paciente en la base de datos : {e}")
