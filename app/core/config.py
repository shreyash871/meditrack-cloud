from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "meditrack"


settings = Settings()
