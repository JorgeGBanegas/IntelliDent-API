from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class DentalImage(Base):
    __tablename__ = "dental_image"
    dental_image_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"))
    patient = relationship("Patient", back_populates="images")
    path = Column(String)
    title = Column(String)
    image_category_id = Column(Integer, ForeignKey("image_category.image_category_id"))
    category = relationship("ImageCategory", back_populates="images")
    teeth = relationship("Tooth", secondary="image_tooth", back_populates="images")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=None)
