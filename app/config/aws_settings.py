import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AwsSetting(BaseSettings):
    check_expiration: bool = True
    jwt_header_prefix: str = "Bearer"
    jwt_header_name: str = "Authorization"
    userpools: dict = {
        "sa": {
            "region": os.getenv("AWS_REGION"),
            "userpool_id": os.getenv("AWS_USER_POOL_ID"),
            "app_client_id": os.getenv("AWS_APP_CLIENT_ID"),
        }
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
