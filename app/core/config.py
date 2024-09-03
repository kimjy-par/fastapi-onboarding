import os
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")

    if ENV == "prod":
        pass
    elif ENV == "staging":
        pass
    elif ENV == "test":
        DB_URL: str = "mariadb+aiomysql://root:root@localhost:3306/test"
    else:
        DB_URL: str = "mariadb+aiomysql://root:root@localhost:3306/mnc_onboarding"

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDER: str = "asc"
    ORDER_COLUMN: str = "id"


configs = Configs()
