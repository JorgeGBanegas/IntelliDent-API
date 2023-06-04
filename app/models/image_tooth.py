from sqlalchemy import Table, Integer, ForeignKey, Column

from app.config.database import Base

image_tooth = Table(
    "image_tooth", Base.metadata,
    Column("image_id", Integer, ForeignKey("dental_image.dental_image_id"), primary_key=True),
    Column("tooth_id", Integer, ForeignKey("tooth.tooth_id"), primary_key=True)
)
