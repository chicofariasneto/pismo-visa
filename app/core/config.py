from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and the ``.env`` file.

    All ``POSTGRES_*`` fields are required (no defaults) so the application
    fails fast at startup if the database is not configured.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Pismo Visa API"
    app_version: str = "0.1.0"
    debug: bool = False

    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str

    @computed_field
    @property
    def database_url(self) -> str:
        """Build the async SQLAlchemy database URL from individual connection fields.

        :returns: A ``postgresql+asyncpg://`` connection string.
        :rtype: str
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
