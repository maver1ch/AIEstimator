from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Estimating Assistant"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = "ai_estimator"
    POSTGRES_PASSWORD: str = "ai_estimator_password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "estimator_db"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # LLM Settings
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    MODEL_NAME: str = "claude-3-5-sonnet-20240620"

    class Config:
        env_file = ".env"

settings = Settings()
