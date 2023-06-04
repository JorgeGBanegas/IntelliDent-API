from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.models.tooth import Tooth
from app.models.image_tooth import image_tooth


class ToothService:
    def __init__(self, db: Session):
        self.db = db

    def get_tooth_by_id(self, tooth_id: int):
        try:
            tooth = self.db.query(Tooth).get(tooth_id)
            if tooth is None:
                raise RecordNotFoundException("No se encontró el diente")
            return tooth

        except RecordNotFoundException:
            raise
        except Exception as e:
            raise ValueError(f"Error al obtener diente: {e}")