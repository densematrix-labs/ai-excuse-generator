"""Application configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App settings
    app_name: str = "AI Excuse Generator"
    debug: bool = False
    
    # LLM Proxy settings
    llm_proxy_url: str = "https://llm-proxy.densematrix.ai"
    llm_proxy_key: str = "sk-wskhgeyawc"
    llm_model: str = "gemini-3-flash-preview"
    
    # Database settings
    database_url: Optional[str] = None
    
    # Creem payment settings
    creem_api_key: Optional[str] = None
    creem_webhook_secret: Optional[str] = None
    creem_product_id_10: Optional[str] = None
    creem_product_id_30: Optional[str] = None
    creem_product_id_unlimited: Optional[str] = None
    
    # Free trial settings
    free_trial_count: int = 1
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
