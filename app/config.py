from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "deepagent_memory.db"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"

load_dotenv(ROOT_DIR / ".env")


class Settings(BaseSettings):
    app_name: str = "MCP DeepAgent Workbench"
    database_path: Path = DB_PATH
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

