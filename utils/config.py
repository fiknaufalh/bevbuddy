from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_sslmode: str
    db_port: str
    db_name: str
    secret_key: str
    algorithm: str
    admin_token: str
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()