from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.odontogram_controller import OdontogramController
from app.schemas.detail_odontogram_schema import DetailOdontogramItem, DetailOdontogramCreate
from app.schemas.odontogram_schema import Odontogram, OdontogramCreate

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/odontograms",
    tags=["odontogram"]
)


@router.get("/patient/{patient_id}", response_model=list[Odontogram], status_code=200)
def get_odontogram_by_patient_id(patient_id: int, odontogram_controller: OdontogramController = Depends(),
                                 auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return odontogram_controller.get_odontogram_by_patient_id(patient_id)


@router.get("/{odontogram_id}", response_model=None, status_code=200)
def get_odontogram_by_id(odontogram_id: int, odontogram_controller: OdontogramController = Depends(),
                         auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return odontogram_controller.get_odontogram_by_id(odontogram_id)


@router.post("/", response_model=Odontogram, status_code=201)
def create_odontogram(odontogram: OdontogramCreate, odontogram_controller: OdontogramController = Depends(),
                      auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return odontogram_controller.create_odontogram(odontogram)


@router.get("/{odontogram_id}/tooth/{tooth_number}", response_model=list[DetailOdontogramItem], status_code=200)
def get_detail_odontogram(odontogram_id: int, tooth_number: int, page: int = 0, limit: int = 0,
                          odontogram_controller: OdontogramController = Depends(),
                          auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return odontogram_controller.get_detail_odontogram(odontogram_id, tooth_number, page, limit)


@router.post("/details", response_model=None, status_code=201)
def create_detail_odontogram(detail_odontogram: DetailOdontogramCreate,
                             odontogram_controller: OdontogramController = Depends(),
                             auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return odontogram_controller.create_detail_odontogram(detail_odontogram)
