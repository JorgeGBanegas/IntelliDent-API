from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.image_process_service import ImageProcessService
from app.services.patient_service import PatientService


def get_patient_service(db: Session = Depends(get_db)):
    return PatientService(db)


def get_image_process_service(db: Session = Depends(get_db)):
    return ImageProcessService(db)
