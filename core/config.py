
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(Path(__file__).parent.parent / ".env"))

    database_url: str
    secret_key:str
    test_database_url:str | None = None
    db_schema: str = "ecommerce"
    cors_origins: list[str] = ["http://localhost:5173"]

settings = Settings() # type: ignore