from fastapi import APIRouter, UploadFile, Depends, Header
from fastapi_cognito import CognitoAuth, CognitoSettings
from starlette import status

from app.config.aws_settings import AwsSetting
from app.controllers.image_process_controller import ImageProcessController

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/radiographic-images",
    tags=["radiographic-images"]
)


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
async def analyze_x_ray(image_file: UploadFile, image_process_controller: ImageProcessController = Depends(),
                        authorization: str = Header(...), auth: CognitoAuth = Depends(cognito_sa.auth_required)):
    image = image_file.file.read()
    # Get the token from the header
    images = await image_process_controller.analyze_x_ray(image, authorization)
    return images
