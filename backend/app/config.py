from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM Proxy
    llm_proxy_url: str = "https://llm-proxy.densematrix.ai"
    llm_proxy_key: str = ""
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./excuse.db"
    
    # Creem Payment
    creem_api_key: str = ""
    creem_webhook_secret: str = ""
    creem_product_ids: str = ""  # JSON string
    
    # App
    debug: bool = False
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
