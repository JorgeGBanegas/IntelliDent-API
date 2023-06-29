from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException, InvalidDataException
from app.models import Odontogram
from app.schemas.odontogram_schema import Odontogram as OdontogramSchema, OdontogramCreate


class OdontogramService:
    def __init__(self, db: Session):
        self.db = db

    def get_odontogram_by_id(self, odontogram_id: int) -> Odontogram:
        try:
            odontogram = self.db.query(Odontogram).get(odontogram_id)
            if not odontogram:
                raise RecordNotFoundException(
                    f"El odontograma con id {odontogram_id} no se encuentra registrado en la base de datos")
            return odontogram
        except RecordNotFoundException:
            raise
        except Exception as e:
            raise ValueError(f"Error al obtener odontograma de la base de datos : {e}")

    def get_detail_teeth(self, details):
        teeth = []
        for detail in details:
            tooth = detail.tooth
            if not any(t.tooth_id == tooth.tooth_id for t in teeth):
                teeth.append(tooth)
        return teeth

    def get_odontogram_by_patient_id(self, patient_id: int) -> list[OdontogramSchema]:
        try:
            odontograms = self.db.query(Odontogram).filter(Odontogram.patient_id == patient_id).all()
            odontograms_list = [OdontogramSchema(odontogram_id=odontogram.odontogram_id,
                                                 patient_id=odontogram.patient_id,
                                                 type_odontogram_id=odontogram.type_odontogram_id,
                                                 details=self.get_detail_teeth(odontogram.details),
                                                 created_at=odontogram.created_at)
                                for odontogram in odontograms]
            return odontograms_list
        except Exception as e:
            raise ValueError(f"Error al obtener odontograma de la base de datos : {e}")

    def create_odontogram(self, odontogram: OdontogramCreate) -> Odontogram:
        try:
            odontogram_db = Odontogram(**odontogram.dict())
            self.db.add(odontogram_db)
            self.db.commit()
            self.db.refresh(odontogram_db)
            return odontogram_db
        except IntegrityError:
            raise RecordNotFoundException(f"Verifique que el paciente y el tipo de odontograma existan")
        except Exception as e:
            raise ValueError(f"Error al crear odontograma en la base de datos : {e}")
