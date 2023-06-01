from fastapi import Depends, HTTPException
from starlette import status
from starlette.responses import Response

from app.dependencies.dependencies import get_image_process_service
from app.services.image_process_service import ImageProcessService


class ImageProcessController:
    def __init__(self, image_process_service: ImageProcessService = Depends(get_image_process_service)):
        self.image_process_service = image_process_service

    async def analyze_x_ray(self, image_file, auth):
        try:
            token = auth.split("Bearer ")[1]
            inference, enhanced_image = await self.image_process_service.analyze_x_ray(image_file, token)
            # Create the ZIP file in memory
            zip_data = await self.image_process_service.convert_to_zip(enhanced_image)
            # Create the response with the ZIP file
            response = Response(content=zip_data, media_type="application/zip")
            response.headers["Content-Disposition"] = 'attachment; filename="processed_images.zip"'

            # Add inference data as custom headers
            response.headers["X-Inference-Diagnosis"] = str(inference["diagnosis"])
            response.headers["X-Inference-Probability"] = str(inference["probability"])

            return response

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                "message": "Error al analizar imagen",
                "error": str(e)
            })
