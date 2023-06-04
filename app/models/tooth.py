from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class Tooth(Base):
    __tablename__ = "tooth"
    tooth_id = Column(Integer, primary_key=True, index=True)
    tooth_name = Column(String(50))
    numeration = Column(Integer)
    description = Column(String(255), nullable=True)
    images = relationship("DentalImage", secondary="image_tooth", back_populates="teeth")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=None)
