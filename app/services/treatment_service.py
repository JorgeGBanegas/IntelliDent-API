from sqlalchemy.orm import Session

from app.models import Treatment
from app.schemas.treatment_schema import TreatmentCreate


class TreatmentService:
    def __init__(self, db: Session):
        self.db = db

    def add_treatment(self, treatment: TreatmentCreate) -> Treatment:
        try:
            new_treatment = Treatment(**treatment.dict())
            self.db.add(new_treatment)
            self.db.commit()
            self.db.refresh(new_treatment)
            return new_treatment
        except Exception as e:
            raise ValueError(f"Error al guardar tratamiento en la base de datos : {e}")

    def get_all_treatments(self, search: str):
        try:
            query = self.db.query(Treatment)

            if search:
                query = query.filter(Treatment.name_treatment.ilike(f"%{search}%"))

            treatments = query.all()
            treatments_list = [Treatment(treatment_id=treatment.treatment_id,
                                         name_treatment=treatment.name_treatment,
                                         description=treatment.description,
                                         created_at=treatment.created_at,
                                         deleted_at=treatment.deleted_at
                                         ) for treatment in treatments]
            return treatments_list
        except Exception as e:
            raise ValueError(f"Error al obtener tratamientos de la base de datos : {e}")
