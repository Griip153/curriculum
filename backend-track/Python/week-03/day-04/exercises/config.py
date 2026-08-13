from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Students API"
    debug: bool = False
    database_url: str = "sqlite:///./students.db"

    class Config:
        env_file = ".env"


settings = Settings()
