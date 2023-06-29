from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.odontogram_controller import OdontogramController
from app.schemas.odontogram_schema import Odontogram, OdontogramCreate

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/odontograms",
    tags=["odontogram"]
)


@router.get("/patient/{patient_id}", response_model=list[Odontogram], status_code=200)
def get_odontogram_by_patient_id(patient_id: int, odontogram_controller: OdontogramController = Depends()):
    return odontogram_controller.get_odontogram_by_patient_id(patient_id)


@router.get("/{odontogram_id}", response_model=Odontogram, status_code=200)
def get_odontogram_by_id(odontogram_id: int, odontogram_controller: OdontogramController = Depends()):
    return odontogram_controller.get_odontogram_by_id(odontogram_id)


@router.post("/", response_model=Odontogram, status_code=201)
def create_odontogram(odontogram: OdontogramCreate, odontogram_controller: OdontogramController = Depends()):
    return odontogram_controller.create_odontogram(odontogram)
