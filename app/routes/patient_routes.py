from fastapi import APIRouter, status, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.patient_controller import PatientController
from app.schemas.patient_schema import PatientCreate, Patient, PatientUpdate, PatientItemList

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/patients",
    tags=["patient"]
)


# route for create a new patient
@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def add_patient(patient: PatientCreate, patient_controller: PatientController = Depends(),
                auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    user_id = str(auth).split(' ')[1].split('=')[1]
    user_id = user_id.strip("'")
    return patient_controller.add_patient(patient, user_id)


# route for get all patients with pagination
@router.get("/", response_model=list[PatientItemList], status_code=status.HTTP_200_OK)
def get_all_patients(search_query: str = None, page: int = 0, limit: int = 50,
                     patient_controller: PatientController = Depends()):
    return patient_controller.get_all_patients(search_query, page, limit)


@router.get("/{patient_id}", response_model=Patient, status_code=status.HTTP_200_OK)
def get_patient_by_id(patient_id: str, patient_controller: PatientController = Depends(),
                      auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return patient_controller.get_patient_by_id(patient_id)


@router.put("/{patient_id}", response_model=Patient, status_code=status.HTTP_200_OK)
def update_patient(patient_id: str, patient_update: PatientUpdate, patient_controller: PatientController = Depends(),
                   auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return patient_controller.update_patient(patient_id, patient_update)
