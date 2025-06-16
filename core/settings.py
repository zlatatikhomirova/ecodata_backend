from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from s3_storage.minio import S3StorageSettings
from database.config.db_settings import DBSettings


class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    s3_settings: S3StorageSettings = S3StorageSettings()
    # secret_key: str
    # access_token_expire_minutes: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


settings = Settings()
