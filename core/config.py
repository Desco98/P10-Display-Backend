from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_USE_TLS: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
