from fastapi import APIRouter, Depends
from fastapi_cognito import CognitoAuth, CognitoSettings

from app.config.aws_settings import AwsSetting
from app.controllers.image_category_controller import ImageCategoryController
from app.schemas.image_category_schema import ImageCategory

aws_settings = AwsSetting()
cognito_sa = CognitoAuth(settings=CognitoSettings.from_global_settings(aws_settings), userpool_name="sa")

router = APIRouter(
    prefix="/images-category",
    tags=["images-category"]
)


@router.get("/", response_model=list[ImageCategory])
async def get_all_dental_images_by_patient_and_category(image_category_controller: ImageCategoryController = Depends()):
    return image_category_controller.get_all_categories()