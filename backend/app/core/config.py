from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Resume Analyzer API"
    admin_email: str = "admin@resume-analyzer.com"
    secret_key: str = "super-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()