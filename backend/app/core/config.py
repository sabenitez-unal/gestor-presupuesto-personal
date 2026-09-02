from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    
    class ConfigDict:
        env_file = ".env"

settings = Settings() # type: ignore
