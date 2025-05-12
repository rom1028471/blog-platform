from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    APP_NAME: str = "BlogNest API"
    POSTGRES_URL: str = "postgresql://postgres:postgres@localhost:5432/bsdb"
    JWT_SECRET: str = "v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShVkYp"
    JWT_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"

settings = Settings()