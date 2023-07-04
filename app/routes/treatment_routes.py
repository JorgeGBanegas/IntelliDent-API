from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.treatment_controller import TreatmentController
from app.schemas.treatment_schema import Treatment, TreatmentCreate

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/treatments",
    tags=["treatments"]
)


@router.get("/", response_model=list[Treatment], status_code=200)
def get_all_treatments(search: str = None, treatment_controller: TreatmentController = Depends()):
    return treatment_controller.get_all_treatments(search)


@router.post("/", response_model=None, status_code=201)
def add_treatment(treatment: TreatmentCreate, treatment_controller: TreatmentController = Depends()):
    return treatment_controller.add_treatment(treatment)
