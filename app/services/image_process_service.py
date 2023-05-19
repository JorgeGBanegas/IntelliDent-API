import io

from PIL import Image

import cv2
import numpy as np
from numpy import ndarray
from sqlalchemy.orm import Session


class ImageProcessService:
    def __init__(self, db: Session):
        self.db = db

    async def analyze_x_ray(self, image_file) -> bytes:
        crop_image = self._crop_image(image_file)
        enhance_image = self._enhance_image(crop_image)
        enhance_image = self._convert_ndarray_to_image(enhance_image)
        return enhance_image

    @staticmethod
    def _convert_ndarray_to_image(enhance_image):
        image = Image.fromarray(enhance_image)
        byte_stream = io.BytesIO()
        image.save(byte_stream, format="JPEG")
        byte_stream.seek(0)
        return byte_stream.read()

    @staticmethod
    def _crop_image(image_file) -> ndarray:
        # load the image
        image_array = np.frombuffer(image_file, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        # Calculate the aspect ratio of the original image
        original_height, original_width, _ = image.shape
        aspect_ratio = original_width / original_height

        # Set the desired width for display
        screen_width = 800

        # Calculate the corresponding height to maintain the aspect ratio
        screen_height = int(screen_width / aspect_ratio)

        # Resize the image to fit the screen
        resized_image = cv2.resize(image, (screen_width, screen_height))

        # Convert the resized image to grayscale
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, 80, 150)

        # Find contours in the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area (periapical radiograph)
        largest_contour = max(contours, key=cv2.contourArea)

        # Create a mask from the largest contour
        mask = np.zeros_like(edges)
        cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

        # Bitwise-AND the resized image with the mask to get the cropped radiograph
        cropped_image = cv2.bitwise_and(resized_image, resized_image, mask=mask)

        # Find the bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Adjust the bounding rectangle coordinates based on the resizing
        x = int(x * original_width / screen_width)
        y = int(y * original_height / screen_height)
        w = int(w * original_width / screen_width)
        h = int(h * original_height / screen_height)

        # Crop the original image using the adjusted bounding rectangle coordinates
        cropped_original_image = image[y:y + h, x:x + w].copy()

        return cropped_original_image

    @staticmethod
    def _enhance_image(image) -> ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # normalize the image
        normalized = np.zeros((800, 800))
        normalized = cv2.normalize(gray, normalized, 0, 255, cv2.NORM_MINMAX)

        # Apply histogram equalization
        equalized = cv2.equalizeHist(normalized)

        # Apply Median filter
        median_filter = cv2.medianBlur(equalized, 5)

        return median_filter
