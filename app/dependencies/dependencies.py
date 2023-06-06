from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.dental_image_service import DentalImageService
from app.services.image_category_service import ImageCategoryService
from app.services.image_process_service import ImageProcessService
from app.services.patient_service import PatientService


def get_patient_service(db: Session = Depends(get_db)):
    return PatientService(db)


def get_image_process_service(db: Session = Depends(get_db)):
    return ImageProcessService(db)


def get_dental_image_service(db: Session = Depends(get_db)):
    return DentalImageService(db)


def get_image_category_service(db: Session = Depends(get_db)):
    return ImageCategoryService(db)
