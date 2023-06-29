from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.config.database import Base


class TypeOdontogram(Base):
    __tablename__ = "type_odontogram"
    type_odontogram_id = Column(Integer, primary_key=True, index=True)
    name_type = Column(String, nullable=False)
    odontogram = relationship("Odontogram", back_populates="type_odontogram")