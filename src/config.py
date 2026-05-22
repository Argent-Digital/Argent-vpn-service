from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY_FOR_JWT: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    VPN_SERVICE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()