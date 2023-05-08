import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Setting(BaseSettings):
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_driver: str = os.getenv("DB_DRIVER")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self):
        return f"{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
