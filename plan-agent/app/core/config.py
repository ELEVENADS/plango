from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    llm_provider: str = "deepseek"
    llm_model: str = "deepseek-v4-flash"
    llm_api_key: str = ""
    llm_temperature: float = 0.0
    llm_max_tokens: int = 1024

    # Server
    host: str = "localhost"
    port: int = 18000

    # External services
    elasticsearch_url: str = "http://localhost:9200"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
