"""Tests for configuration."""
import pytest
from unittest.mock import patch
import os

from app.config import Settings, get_settings


class TestSettings:
    """Tests for Settings class."""
    
    def test_default_values(self):
        """Should have correct default values."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.app_name == "AI Excuse Generator"
            assert settings.debug == False
            assert settings.llm_proxy_url == "https://llm-proxy.densematrix.ai"
            assert settings.llm_model == "gemini-3-flash-preview"
            assert settings.free_trial_count == 1
    
    def test_env_override(self):
        """Should allow environment variable overrides."""
        with patch.dict(
            os.environ,
            {"DEBUG": "true", "LLM_MODEL": "gpt-4o"},
            clear=False,
        ):
            settings = Settings()
            
            assert settings.debug == True
            assert settings.llm_model == "gpt-4o"
    
    def test_optional_fields(self):
        """Optional fields should default to None."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.database_url is None
            assert settings.creem_api_key is None


class TestGetSettings:
    """Tests for get_settings function."""
    
    def test_returns_settings(self):
        """Should return a Settings instance."""
        # Clear the cache first
        get_settings.cache_clear()
        
        settings = get_settings()
        
        assert isinstance(settings, Settings)
    
    def test_returns_cached_instance(self):
        """Should return the same cached instance."""
        get_settings.cache_clear()
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2
