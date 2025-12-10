from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    
    SECRET_KEY: str = "changethis" # Default for dev, user should override
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    HF_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"

settings = Settings()
