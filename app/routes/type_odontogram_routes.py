from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.type_odontogram_controller import TypeOdontogramController
from app.schemas.type_odontogram_schema import TypeOdontogram

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/types_odontograms",
    tags=["types odontograms"]
)


@router.get("/", response_model=list[TypeOdontogram], status_code=200)
def get_all_type_odontogram(type_odontogram_controller: TypeOdontogramController = Depends()):
    return type_odontogram_controller.get_all_type_odontogram()

