from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

SOURCE_DIR = Path(__file__).resolve().parent.parent.parent


class GeminiConfig(BaseModel):
    api_key: str


class TgConfig(BaseModel):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__",
        env_file=(SOURCE_DIR / ".env",),
        extra="ignore",
    )
    tg_bot: TgConfig
    gemini: GeminiConfig


print(SOURCE_DIR)
settings = Settings()
print(settings.tg_bot.token)
