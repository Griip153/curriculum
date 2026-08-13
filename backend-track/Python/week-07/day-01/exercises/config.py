from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Students API"
    debug: bool = False
    database_url: str = "sqlite:///./students.db"
    jwt_secret_key: str = "dev-only-secret-change-me"
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = "noreply@studentsapi.test"
    mail_port: int = 2525
    mail_server: str = "sandbox.smtp.mailtrap.io"

    class Config:
        env_file = ".env"


settings = Settings()
