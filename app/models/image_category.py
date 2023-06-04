from sqlalchemy import Column, String, Integer, func, TIMESTAMP
from sqlalchemy.orm import relationship

from app.config.database import Base


class ImageCategory(Base):
    __tablename__ = "image_category"
    image_category_id = Column(Integer, primary_key=True, index=True)
    image_category_name = Column(String(50))
    description = Column(String(255))
    images = relationship("DentalImage", back_populates="category")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=None)
