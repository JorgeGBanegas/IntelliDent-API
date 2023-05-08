from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import Setting

SQLALCHEMY_DATABASE_URL = Setting().db_url

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("Conexión a la base de datos exitosa")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
