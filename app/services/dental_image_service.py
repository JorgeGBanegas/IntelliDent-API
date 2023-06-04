import base64
import binascii
from datetime import datetime

import boto3
from sqlalchemy.exc import DatabaseError, OperationalError, IntegrityError
from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.config.aws_settings import AwsSetting
from app.models.dental_image import DentalImage
from app.schemas.dental_image_schema import DentalImageItemList, DentalImageCreate
from app.services.tooth_service import ToothService


class DentalImageService:
    def __init__(self, db: Session):
        self.db = db

    # Get all image of a patient
    def get_all_dental_images_by_patient_and_category(self, patient_id: int, category_id: int):
        try:
            query = self.db.query(DentalImage).filter(DentalImage.patient_id == patient_id,
                                                      DentalImage.image_category_id == category_id)

            images = query.all()
            images_list = [DentalImageItemList(dental_image_id=image.dental_image_id, path=image.path,
                                               title=image.title) for image in images]
            return images_list
        except Exception as e:
            raise ValueError(f"Error al obtener imagenes: {e}")

    def save_dental_images(self, image_data: DentalImageCreate):
        try:
            aws_settings = AwsSetting()
            bucket = aws_settings.aws_bucket_name
            s3 = boto3.client('s3')
            image_file = image_data.image_file
            image_urls = []
            images = []
            patient_id = image_data.patient_id
            category_id = image_data.image_category_id
            try:
                for image in image_file:
                    # decode image base64
                    image_b64 = base64.b64decode(image.image_base64)
                    image_name = datetime.now().strftime("%Y%m%d%H%M%S%f") + '.jpg'
                    new_image = DentalImage(path='', title=image.title, patient_id=patient_id,
                                            image_category_id=category_id)

                    for tooth in image.teeth:
                        tooth_id = tooth
                        new_image.teeth.append(ToothService(self.db).get_tooth_by_id(tooth_id))

                    s3.put_object(Body=image_b64, Bucket=bucket, Key=image_name, ACL='public-read')
                    image_url = f"https://{bucket}.s3.amazonaws.com/{image_name}"
                    image_urls.append(image_url)

                    new_image.path = image_url
                    images.append(new_image)

                self.db.add_all(images)
                self.db.commit()
                return {
                    "message": "Imagenes guardadas correctamente",
                    "data": image_urls
                }
            except RecordNotFoundException:
                raise

            except IntegrityError:
                self.db.rollback()
                self._rollback_s3(bucket, image_urls, s3)
                raise ValueError(f"Error al guardar, verifique que el paciente, categoria y/o dientes sean "
                                 f"validos ")

            except binascii.Error as e:
                self.db.rollback()
                self._rollback_s3(bucket, image_urls, s3)
                raise ValueError(f"Error al decodificar la imagen base64 {e}")

            except Exception as e:
                self.db.rollback()
                self._rollback_s3(bucket, image_urls, s3)
                raise ValueError(f"Error al guardar imagen: {e}")

        except (DatabaseError, OperationalError) as e:
            raise ValueError(f"Error al iniciar transacción: {e}")
        finally:
            self.db.close()

    def _rollback_s3(self, bucket, image_urls, s3):
        for image_url in image_urls:
            s3.delete_object(Bucket=bucket, Key=image_url.split('/')[-1])
