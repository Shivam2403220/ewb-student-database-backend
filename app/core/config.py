from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Student Database Backend"
    database_url: str = "sqlite:///./data/students.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    chroma_path: str = "./data/chroma"
    allowed_origins: str = "*"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
