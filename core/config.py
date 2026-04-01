
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key:str
    test_database_url:str
    class Config:
        env_file = ".env"

settings = Settings() # type: ignore

'''
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()
'''