from fastapi import APIRouter, status, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.patient_controller import PatientController
from app.schemas.patient_schema import PatientCreate

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
