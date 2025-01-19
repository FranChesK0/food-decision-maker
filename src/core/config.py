import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__)).removesuffix(
    os.path.join("src", "core")
)


class Settings(BaseSettings):
    """
    Settings class for the application.

    Attributes:
        BASE_DIR (str): The base directory of the application.
        HOST (str): The host of the application.
        PORT (int): The port of the application.
        FOOD_DELIVERY_BASE_URL (str): The base URL of the food delivery service.
    """

    BASE_DIR: str = BASE_DIR
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    FOOD_DELIVERY_BASE_URL: str = "http://90.156.171.75:8000"

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"))


settings = Settings()
