from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

basepath = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    mongo_username: str
    mongo_password: str
    mongo_host: str
    server_internal_port: int
    server_internal_host: str
    server_external_port: int
    logging_dir_path: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=basepath / ".env",
        case_sensitive=False,
        extra="ignore",
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore
