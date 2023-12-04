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

    # VCC API
    vcc_api_url: str
    vcc_username: str
    vcc_password: str

    class Config:
        env_file = ".env"

settings = Settings()