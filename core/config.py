
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(Path(__file__).parent.parent / ".env"))
    
    database_url: str
    secret_key:str
    test_database_url:str

settings = Settings() # type: ignore