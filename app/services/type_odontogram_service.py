from sqlalchemy.orm import Session

from app.models import TypeOdontogram
from app.schemas.type_odontogram_schema import TypeOdontogram as TypeOdontogramSchema


class TypeOdontogramService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_type_odontogram(self) -> list[TypeOdontogramSchema]:
        try:
            type_odontograms = self.db.query(TypeOdontogram).all()
            type_odontograms_list = [TypeOdontogramSchema(type_odontogram_id=type_odontogram.type_odontogram_id,
                                                          name_type=type_odontogram.name_type)
                                     for type_odontogram in type_odontograms]
            return type_odontograms_list
        except Exception as e:
            raise ValueError(f"Error al obtener tipos de odontograma de la base de datos : {e}")
