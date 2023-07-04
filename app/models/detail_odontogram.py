from sqlalchemy import Column, Integer, String, func, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class DetailOdontogram(Base):
    __tablename__ = "detail_odontogram"
    detail_odontogram_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=True)
    odontogram_id = Column(Integer, ForeignKey("odontogram.odontogram_id"), primary_key=True)
    odontogram = relationship("Odontogram", back_populates="details")
    tooth_id = Column(Integer, ForeignKey("tooth.tooth_id"), nullable=False)
    tooth = relationship("Tooth", back_populates="details")
    treatment_id = Column(Integer, ForeignKey("treatment.treatment_id"), nullable=False)
    treatment = relationship("Treatment", back_populates="details")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
