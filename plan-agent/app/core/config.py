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

    # Nacos
    nacos_server_addr: str = "localhost:8848"
    nacos_service_name: str = "plan-agent"
    nacos_service_ip: str = ""
    nacos_service_port: int = 18000
    nacos_group: str = "DEFAULT_GROUP"

    # External services
    elasticsearch_url: str = "http://localhost:9200"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
