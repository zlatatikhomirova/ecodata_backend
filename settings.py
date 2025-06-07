from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from storage.minio import S3StorageSettings


class DBSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    s3_settings: S3StorageSettings = S3StorageSettings()
    # secret_key: str
    # access_token_expire_minutes: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


settings = Settings()
