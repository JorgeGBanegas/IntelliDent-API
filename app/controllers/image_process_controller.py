import io

from fastapi import Depends, HTTPException
from starlette import status
from starlette.responses import StreamingResponse

from app.dependencies.dependencies import get_image_process_service
from app.services.image_process_service import ImageProcessService


class ImageProcessController:
    def __init__(self, image_process_service: ImageProcessService = Depends(get_image_process_service)):
        self.image_process_service = image_process_service

    async def analyze_x_ray(self, image_file):
        try:
            enhanced_image = await self.image_process_service.analyze_x_ray(image_file)
            return StreamingResponse(io.BytesIO(enhanced_image), media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al analizar imagen",
                "error": str(e)
            })
