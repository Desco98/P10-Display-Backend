from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    MQTT_USE_TLS: bool

    class Config:
        env_file = ".env"

settings = Settings()
