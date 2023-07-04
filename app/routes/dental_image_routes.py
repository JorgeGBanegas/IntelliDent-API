from typing import List

from fastapi import APIRouter, UploadFile, Depends, Body, File, Form
from fastapi_cognito import CognitoAuth, CognitoSettings
from starlette import status

from app.config.aws_settings import AwsSetting
from app.controllers.dental_image_controller import DentalImageController
from app.schemas.dental_image_schema import DentalImageCreate, DentalImageItemList

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/dental-images",
    tags=["dental-images"]
)


# Get all image of a patient
@router.get("/", response_model=None)
async def get_all_dental_images_by_patient_and_category(patient_id: int, category_id: int,
                                                        dental_image_controller: DentalImageController = Depends(),
                                                        auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return dental_image_controller.get_all_dental_images_by_patient_and_category(patient_id, category_id)


# Save image
@router.post("/xrays", status_code=status.HTTP_201_CREATED)
async def save_dental_image(image_file: DentalImageCreate, dental_image_controller: DentalImageController = Depends(),
                            auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return dental_image_controller.save_dental_images(image_file)


# Get all image of a patient by tooth
@router.get("/tooth", response_model=list[DentalImageItemList])
async def get_all_image_patient_by_tooth(patient_id: int, tooth_number: int,
                                         dental_image_controller: DentalImageController = Depends(),
                                         ):
    return dental_image_controller.get_all_image_patient_by_tooth(patient_id, tooth_number)


# Get all image of a patient
@router.get("/patient", response_model=list[DentalImageItemList])
async def get_all_images_by_patient(patient_id: int, dental_image_controller: DentalImageController = Depends()):
    return dental_image_controller.get_all_images_by_patient(patient_id)
