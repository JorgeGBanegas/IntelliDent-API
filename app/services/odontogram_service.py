from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.models import Odontogram, DetailOdontogram
from app.schemas.odontogram_schema import Odontogram as OdontogramSchema, OdontogramCreate
from app.schemas.detail_odontogram_schema import DetailOdontogramItem as DetailOdontogramItemSchema, \
    DetailOdontogramCreate, DetailOdontogramBase
from app.services.tooth_service import ToothService


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

    # noinspection PyTypeChecker
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

    # noinspection PyTypeChecker
    def get_detail_odontogram(self, odontogram_id: int, tooth_number: int, page: int, limit: int) \
            -> list[DetailOdontogramItemSchema]:
        try:
            query_tooth = ToothService(self.db).get_tooth_by_number(tooth_number)
            query_detail = self.db.query(DetailOdontogram).filter(
                DetailOdontogram.odontogram_id == odontogram_id,
                DetailOdontogram.tooth_id == query_tooth.tooth_id).order_by(desc(DetailOdontogram.created_at))

            if limit > 0:
                detail_odontogram = query_detail.offset(page * limit).limit(limit).all()

            else:
                detail_odontogram = query_detail.all()

            list_detail_odontogram = [DetailOdontogramItemSchema(detail_odontogram_id=detail.detail_odontogram_id,
                                                                 description=detail.description,
                                                                 odontogram_id=detail.odontogram_id,
                                                                 tooth=detail.tooth,
                                                                 treatment=detail.treatment,
                                                                 created_at=detail.created_at)
                                      for detail in detail_odontogram]

            return list_detail_odontogram
        except RecordNotFoundException:
            raise
        except Exception as e:
            print(e)
            raise ValueError(f"Error al obtener odontograma de la base de datos : {e}")

    def create_detail_odontogram(self, detail_odontogram: DetailOdontogramCreate) -> DetailOdontogram:
        try:
            tooth_number = detail_odontogram.tooth_number
            tooth = ToothService(self.db).get_tooth_by_number(tooth_number)
            detail_base = DetailOdontogramBase(
                description=detail_odontogram.description,
                odontogram_id=detail_odontogram.odontogram_id,
                tooth_id=tooth.tooth_id,
                treatment_id=detail_odontogram.treatment_id
            )
            detail = DetailOdontogram(**detail_base.dict())
            self.db.add(detail)
            self.db.commit()
            self.db.refresh(detail)

            return detail
        except RecordNotFoundException:
            raise
        except IntegrityError:
            raise RecordNotFoundException(f"Verifique que el odontograma y el diente existan")
        except Exception as e:
            raise ValueError(f"Error al crear detalle odontograma en la base de datos : {e}")