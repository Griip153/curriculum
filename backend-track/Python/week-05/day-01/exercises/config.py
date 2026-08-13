from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Students API"
    debug: bool = False
    database_url: str = "sqlite:///./students.db"
    jwt_secret_key: str = "dev-only-secret-change-me"

    class Config:
        env_file = ".env"


settings = Settings()
