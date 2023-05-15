from typing import List, Type

from sqlalchemy.orm import Session
from app.Exceptions.persistence_exceptions import RecordNotFoundException, RecordAlreadyExistsException, \
    IntegrityErrorException
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientItemList
import logging
from sqlalchemy.exc import IntegrityError

# configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def add_patient(self, patient: PatientCreate, user_id) -> Patient:
        try:
            self._is_patient_registered(patient)
            patient = Patient(**patient.dict())
            patient.created_by = user_id
            self.db.add(patient)
            self.db.commit()
            self.db.refresh(patient)
            return patient

        except RecordAlreadyExistsException:
            raise
        except IntegrityError:
            raise IntegrityErrorException(f"El email {patient.email} ya se encuentra registrado en la base de datos")
        except Exception as e:
            raise ValueError(f"Error al agregar paciente a la base de datos : {e}")

    def _is_patient_registered(self, patient):
        patient_exists = self.db.query(Patient).filter(Patient.first_name == patient.first_name,
                                                       Patient.last_name == patient.last_name,
                                                       Patient.date_of_birth == patient.date_of_birth).first()
        if patient_exists:
            raise RecordAlreadyExistsException(f"El paciente {patient.first_name} {patient.last_name} ya se "
                                               f"encuentra registrado en la base de datos")

    # get al patients with pagination
    def get_all_patients(self, search_query, page, limit) -> list[PatientItemList]:
        try:
            query = self.db.query(Patient).with_entities(Patient.patient_id, Patient.first_name, Patient.last_name,
                                                         Patient.phone_number)
            if search_query:
                query = query.filter(Patient.first_name.ilike(f"%{search_query}%") |
                                     Patient.last_name.ilike(f"%{search_query}%"))

            query = query.order_by(Patient.first_name)
            patients = query.offset(page * limit).limit(limit).all()
            patients_list = [PatientItemList(patient_id=patient.patient_id, first_name=patient.first_name,
                                             last_name=patient.last_name,
                                             phone_number=patient.phone_number) for patient in patients]
            return patients_list
        except Exception as e:
            raise ValueError(f"Error al obtener pacientes de la base de datos : {e}")

    # get patient by id
    def get_patient_by_id(self, patient_id) -> Patient:
        try:
            patient = self.db.query(Patient).get(patient_id)
            if not patient:
                raise RecordNotFoundException(f"No se encontró un paciente con el id especificado")
            return patient
        except RecordNotFoundException as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error al obtener paciente de la base de datos : {e}")

    # update patient
    def update_patient(self, patient_id, patient_update: PatientUpdate) -> Patient:
        try:
            patient = self.db.query(Patient).get(patient_id)
            if not patient:
                raise RecordNotFoundException(f"No se encontró un paciente con el id especificado")

            for var, value in vars(patient_update).items():
                if value is not None:
                    setattr(patient, var, value)
            self.db.commit()
            self.db.refresh(patient)
            return patient
        except RecordNotFoundException as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error al actualizar paciente en la base de datos : {e}")
