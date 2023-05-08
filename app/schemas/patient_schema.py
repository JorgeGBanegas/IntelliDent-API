from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50, example="Jorge")
    last_name: str = Field(..., min_length=3, max_length=50, example="Banegas")
    date_of_birth: date
    gender: str = Field(..., min_length=1, max_length=1, example="M")
    phone_number: str = Field(..., min_length=5, max_length=15, example="70976408")
    email: Optional[EmailStr] = None
    created_by: str = None
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: Optional[datetime] = None

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v > datetime.now().date():
            raise ValueError('La fecha de nacimiento no puede ser posterior a la fecha actual')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['M', 'F']:
            raise ValueError('El género debe ser M o F')
        return v

    class Config:
        orm_mode = True
        validate_assignment = True
        error_msg_templates = {
            'value_error.missing': 'El campo es requerido',
            'value_error.any_str.min_length': 'El campo debe tener al menos {limit_value} caracter/es',
            'value_error.any_str.max_length': 'El campo debe tener como máximo {limit_value} caracter/es',
            'value_error.email': 'El campo debe ser un correo electrónico válido',
            'value_error.date': 'El campo debe ser una fecha válida (YYYY-MM-DD)',
        }


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    firs_name: Optional[str] = Field(None, min_length=3, max_length=50, example="Jorge")
    last_name: Optional[str] = Field(None, min_length=3, max_length=50, example="Banegas")
    date_of_birth: Optional[datetime]
    phone_number: Optional[str] = Field(None, min_length=7, max_length=20, example="504-9999-9999")
    email: Optional[EmailStr] = None
    gender: Optional[str] = Field(None, min_length=1, max_length=1, example="M")
    created_by: Optional[str] = Field(None, min_length=30, max_length=50, example="us-east-1:01234567-89ab-cdef-0123"
                                                                                  "-456789abcdef")
    updated_at: datetime = None


class Patient(PatientBase):
    patient_id: int = Field(..., example=1)
