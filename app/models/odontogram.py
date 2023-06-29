from sqlalchemy import Integer, Column, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Odontogram(Base):
    __tablename__ = "odontogram"
    odontogram_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    patient = relationship("Patient", back_populates="odontogram")
    type_odontogram_id = Column(Integer, ForeignKey("type_odontogram.type_odontogram_id"), nullable=False)
    type_odontogram = relationship("TypeOdontogram", back_populates="odontogram")
    details = relationship("DetailOdontogram", back_populates="odontogram")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now(), onupdate=func.now())