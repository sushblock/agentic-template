from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_provider: str = "openai"
    model_name: str = "gpt-4o-mini"


    openai_api_key: str | None = None
    anthropic_api_key: str | None = None


    ollama_base_url: str = "http://localhost:11434"
    vllm_base_url: str = "http://localhost:8000/v1"


    langchain_tracing_v2: bool = True
    langchain_endpoint: str | None = None
    langchain_api_key: str | None = None
    langchain_project: str = "agentic-template"


    app_env: str = "dev"
    log_level: str = "INFO"

    # ChromaDB settings
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection_name: str = "documents"


    class Config:
        env_file = ".env"


settings = Settings()