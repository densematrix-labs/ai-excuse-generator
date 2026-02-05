"""Application configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import json


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
    creem_product_ids: Optional[str] = None  # JSON string: {"pack_10":"prod_xxx",...}
    
    # Individual product IDs (will be parsed from creem_product_ids)
    creem_product_id_3: Optional[str] = None
    creem_product_id_10: Optional[str] = None
    
    # Free trial settings
    free_trial_count: int = 1
    
    def model_post_init(self, __context) -> None:
        """Parse creem_product_ids JSON into individual fields."""
        if self.creem_product_ids:
            try:
                product_ids = json.loads(self.creem_product_ids)
                if not self.creem_product_id_3:
                    object.__setattr__(self, "creem_product_id_3", product_ids.get("pack_3"))
                if not self.creem_product_id_10:
                    object.__setattr__(self, "creem_product_id_10", product_ids.get("pack_10"))
            except json.JSONDecodeError:
                pass
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
