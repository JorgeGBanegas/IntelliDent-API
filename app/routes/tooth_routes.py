from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.tooth_controller import ToothController
from app.schemas.tooth_schema import Tooth

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/teeth",
    tags=["teeth"]
)


@router.get("/", response_model=list[Tooth])
def get_all_teeth(tooth_controller: ToothController = Depends(),
                  auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return tooth_controller.get_all_teeth()


@router.get("/{tooth_number}", response_model=None)
def get_tooth_by_number(tooth_number: int, tooth_controller: ToothController = Depends(),
                        auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    return tooth_controller.get_tooth_by_number(tooth_number)