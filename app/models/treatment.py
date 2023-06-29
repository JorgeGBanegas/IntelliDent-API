from sqlalchemy import Integer, String, Column, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class Treatment(Base):
    __tablename__ = "treatment"
    treatment_id = Column(Integer, primary_key=True, index=True)
    name_treatment = Column(String, nullable=False)
    description = Column(String, nullable=True)
    details = relationship("DetailOdontogram", back_populates="treatment")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)