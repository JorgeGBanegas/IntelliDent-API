import io
import os
import zipfile
import cv2
import numpy as np
import requests
from fastapi import UploadFile
from numpy import ndarray
from sqlalchemy.orm import Session
from PIL import Image, ImageDraw, ImageFont


class ImageProcessService:
    def __init__(self, db: Session):
        self.db = db

    async def analyze_x_ray(self, image_file, token):

        crop_image = self._crop_image(image_file)
        enhance_image = self._enhance_image(crop_image)
        # Process image
        inference_image, negative_image, magma_image = self._image_process(enhance_image)
        inference_image = self._convert_ndarray_to_image(inference_image)

        inference = self._infer_image(inference_image, token)

        new_enhance_image = self.add_text_to_image(enhance_image, inference)
        images_array = [new_enhance_image, negative_image, magma_image]
        images = []
        for image in images_array:
            image = self._convert_ndarray_to_image(image)
            images.append(image)
        return inference, images

    async def convert_to_zip(self, enhanced_image) -> bytes:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, image_data in enumerate(enhanced_image):
                # Add each image to the ZIP file with a unique name
                filename = f"image_{i}.jpg"
                zip_file.writestr(filename, image_data)
        # Get the bytes from the ZIP file
        zip_data = zip_buffer.getvalue()
        return zip_data

    @staticmethod
    def _infer_image(image, token):
        # get url from env
        url = os.environ.get('ENDPOINT_INFERENCES')

        image_inference = UploadFile(filename="image.jpg", file=image)
        multipart_data = {
            'image_file': ('image.jpg', image_inference.file, 'image/jpeg')
        }
        response = requests.post(url, files=multipart_data)
        if response.status_code != 200:
            raise Exception("Error al realizar la inferencia")

        # Return the response
        return response.json()

    @staticmethod
    def _image_process(image):
        # Resized image for neural network
        inference_image = ImageProcessService._resize_image_png(image, 224, True)

        # Negative image
        negative_image = ImageProcessService._get_negative_image(image)

        # Magma image
        magma_image = ImageProcessService._apply_magma_colormap(image)

        return inference_image, negative_image, magma_image

    @staticmethod
    def _convert_ndarray_to_image(image):
        # Asegurarse de que la imagen tenga el tipo de datos correcto y esté en el rango adecuado
        image = np.clip(image, 0, 255).astype(np.uint8)

        # Convertir la imagen a formato de bytes
        retval, buffer = cv2.imencode('.jpg', image)
        byte_stream = io.BytesIO(buffer)
        return byte_stream.getvalue()

    @staticmethod
    def _crop_image(image_file) -> ndarray:
        # load the image
        image_array = np.frombuffer(image_file, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # median blur for noise reduction
        gray_image = cv2.medianBlur(gray_image, 7)
        gray_image = cv2.bilateralFilter(gray_image, 9, 75, 75)

        # apply adaptive thresholding to get a binary image
        binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11,
                                             2)

        # find the contours from the binary image
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # find the contour with the maximum area
        larger_contour = max(contours, key=cv2.contourArea)

        # get the bounding rectangle of the larger contour
        x, y, w, h = cv2.boundingRect(larger_contour)

        # Create a transparent mask of the size of the original image
        mask = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

        # Draws contour outlines or filled contours.
        cv2.drawContours(mask, [larger_contour], 0, (255, 255, 255, 255), -1)

        # Make sure the original image is RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        # Apply the mask to the original image to get the cropped image with transparent background
        crop_image = cv2.bitwise_and(image, mask)

        # Crop image to the size of the contour
        crop_image = crop_image[y:y + h, x:x + w]

        # get image with transparent background
        return crop_image

    @staticmethod
    def _enhance_image(image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)  # Change color space from RGBA to Grayscale

        # Apply CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(5, 5))
        image_clahe = clahe.apply(gray)

        # Apply bilateral filter to smooth the image
        image_bilateral = cv2.bilateralFilter(image_clahe, 5, 75, 75)

        # create a mask from the alpha channel
        mask = image[:, :, 3]  # Canal alfa de la imagen RGBA

        # create a new image with the same shape as the original image
        result = cv2.cvtColor(image_bilateral, cv2.COLOR_GRAY2BGRA)  # Change from grayscale to BGRA
        result[:, :, 3] = mask  # Assign the mask to the last channel of the new image

        return result

    @staticmethod
    def _resize_image_png(image, size, transparent):
        # load original image
        original_image = image

        # Get original image size
        original_height, original_width = original_image.shape[:2]

        # Define the maximum desired size for the resized image
        max_size = size

        # Calculate the new size keeping the aspect ratio
        if original_height > original_width:
            new_height = max_size
            scale = new_height / original_height
            new_width = int(original_width * scale)
        else:
            new_width = max_size
            scale = new_width / original_width
            new_height = int(original_height * scale)

        # Resizing the image using the new calculated size
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Create a new image with the desired size
        if transparent:
            new_image = np.zeros((max_size, max_size, 4), dtype=np.uint8)
        else:
            new_image = np.zeros((max_size, max_size, 3), dtype=np.uint8)

        # Calculate the coordinates to place the resized image centered on the new image
        x = int((max_size - new_width) / 2)
        y = int((max_size - new_height) / 2)

        # Copy the resized image to the new image preserving the alpha channel if it is transparent
        if transparent:
            new_image[y:y + new_height, x:x + new_width] = resized_image
        else:
            new_image[y:y + new_height, x:x + new_width] = resized_image[:, :, :3]

        return new_image

    # create image negative
    @staticmethod
    def _get_negative_image(image):
        # Get the RGBA channels of the image
        r = image[:, :, 0]
        g = image[:, :, 1]
        b = image[:, :, 2]
        a = image[:, :, 3]

        # Get the negative of the RGB channels
        negative_r = 255 - r
        negative_g = 255 - g
        negative_b = 255 - b

        # Create a new image with the negative channels and the same alpha channel
        negative_image = np.dstack((negative_r, negative_g, negative_b, a))

        return negative_image

    @staticmethod
    def _apply_magma_colormap(image):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

        # Apply the "Magma" colormap to the grayscale image
        colormap_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_MAGMA)

        # Add the alpha channel to the resulting image
        b, g, r = cv2.split(colormap_image)
        alpha = image[:, :, 3]
        colormap_image = cv2.merge((b, g, r, alpha))
        return colormap_image

    @staticmethod
    def add_text_to_image(image, inference):
        try:
            original_height, original_width = image.shape[:2]
            font_size = 12
            fill_color = (0, 0, 255) if inference["diagnosis"] == "Caries" else (0, 255, 0)
            print("Color de texto: ", fill_color)
            text_diagnosis = "Diagnóstico Presuntivo: " + inference["diagnosis"]
            text_probability = "Probabilidad de Caries: " + str(inference["probability"]) + "%"

            while True:
                font = ImageFont.truetype("Montserrat-SemiBold.ttf", font_size)

                width_text, height_text = font.getsize(text_diagnosis)

                if width_text > original_width:
                    break

                font_size += 1

            font = ImageFont.truetype("/app/app/Montserrat-SemiBold.ttf", font_size)

            text = text_diagnosis + "\n" + text_probability
            width_text, height_text = font.getsize(text)

            new_width = original_width + 12
            new_height = original_height + (height_text * 2)

            new_image = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))

            pil_image = Image.fromarray(image)
            new_image.paste(pil_image, (0, 0))

            draw = ImageDraw.Draw(new_image)

            position_x = 0
            position_y = original_height

            draw.text((position_x, position_y), text, font=font, fill=fill_color)
            array_image = np.array(new_image)
            return array_image
        except Exception as e:
            print(e)
            raise e


