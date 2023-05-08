from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.patient_service import PatientService


def get_patient_service(db: Session = Depends(get_db)):
    return PatientService(db)
