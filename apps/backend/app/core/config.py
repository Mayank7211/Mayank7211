from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Local Biz AI Assistant Platform"
    environment: str = "dev"
    api_prefix: str = "/api"
    default_small_model: str = "llama3-8b-8192"
    default_large_model: str = "llama3-70b-8192"
    request_timeout_seconds: int = 15
    max_context_chunks: int = 4
    database_url: str = "sqlite+aiosqlite:///./sql_app.db"
    auto_create_tables: bool = True
    groq_api_key: str = ""
    owner_access_secret: str = "change-me-owner-secret"
    owner_auth_header: str = "X-Owner-Token"
    allowed_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    widget_script_src: str = "https://cdn.your-app.com/widget.js"
    widget_default_theme: str = "light"
    widget_default_position: str = "bottom-right"
    widget_default_primary_color: str = "#0f766e"

    @field_validator("allowed_cors_origins", mode="before")
    @classmethod
    def parse_allowed_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            origins = [origin.strip() for origin in value.split(",") if origin.strip()]
            return origins or ["http://localhost:5173"]
        if isinstance(value, list):
            return [origin for origin in value if origin]
        return ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AI_AGENT_")


settings = Settings()
