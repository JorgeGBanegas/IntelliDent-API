from app.config.database import Base
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, false, func


class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(1))
    date_of_birth = Column(Date())
    phone_number = Column(String(15))
    email = Column(String(50), unique=True, index=True)
    created_by = Column(String(50), nullable=True, server_default=None)
    created_at = Column(TIMESTAMP(timezone=True), nullable=false, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=false, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=None, onupdate=func.now())
