import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.excuse_service import ExcuseService, SCENARIO_PROMPTS, STYLE_INSTRUCTIONS, LANGUAGE_INSTRUCTIONS
from app.schemas.excuse import ExcuseRequest, Scenario, Style


@pytest.mark.asyncio
async def test_generate_excuse_success():
    """Test successful excuse generation."""
    service = ExcuseService()
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Sorry, my cat is having an existential crisis."}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        request = ExcuseRequest(
            scenario=Scenario.SKIP_WORK,
            style=Style.ABSURD,
            device_id="test-device-123456"
        )
        
        result = await service.generate_excuse(request)
        
        assert result == "Sorry, my cat is having an existential crisis."
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_generate_excuse_custom_scenario():
    """Test excuse generation with custom scenario."""
    service = ExcuseService()
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Custom excuse generated."}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        request = ExcuseRequest(
            scenario=Scenario.CUSTOM,
            custom_scenario="need to skip my dentist appointment",
            style=Style.PROFESSIONAL,
            device_id="test-device-123456"
        )
        
        result = await service.generate_excuse(request)
        
        assert result == "Custom excuse generated."


@pytest.mark.asyncio
async def test_generate_excuse_with_target_person():
    """Test excuse generation with target person."""
    service = ExcuseService()
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Boss-appropriate excuse."}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        request = ExcuseRequest(
            scenario=Scenario.LATE_ARRIVAL,
            style=Style.PROFESSIONAL,
            target_person="my boss",
            device_id="test-device-123456"
        )
        
        await service.generate_excuse(request)
        
        call_args = mock_post.call_args
        json_body = call_args.kwargs["json"]
        prompt = json_body["messages"][1]["content"]
        assert "my boss" in prompt


@pytest.mark.asyncio
async def test_generate_excuse_different_languages():
    """Test excuse generation in different languages."""
    service = ExcuseService()
    
    for lang in ["en", "zh", "ja", "de", "fr", "ko", "es"]:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": f"Excuse in {lang}"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            request = ExcuseRequest(
                scenario=Scenario.SKIP_WORK,
                style=Style.SINCERE,
                language=lang,
                device_id="test-device-123456"
            )
            
            await service.generate_excuse(request)
            
            call_args = mock_post.call_args
            json_body = call_args.kwargs["json"]
            prompt = json_body["messages"][1]["content"]
            assert LANGUAGE_INSTRUCTIONS[lang] in prompt


@pytest.mark.asyncio
async def test_generate_excuse_urgency_levels():
    """Test excuse generation with different urgency levels."""
    service = ExcuseService()
    
    urgency_words = ["very low", "low", "medium", "high", "very high"]
    
    for level in range(1, 6):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": f"Urgency {level} excuse"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            request = ExcuseRequest(
                scenario=Scenario.MISS_MEETING,
                style=Style.DRAMATIC,
                urgency=level,
                device_id="test-device-123456"
            )
            
            await service.generate_excuse(request)
            
            call_args = mock_post.call_args
            json_body = call_args.kwargs["json"]
            prompt = json_body["messages"][1]["content"]
            assert urgency_words[level - 1] in prompt


def test_scenario_prompts_completeness():
    """Test all scenarios have prompts."""
    for scenario in Scenario:
        assert scenario in SCENARIO_PROMPTS


def test_style_instructions_completeness():
    """Test all styles have instructions."""
    for style in Style:
        assert style in STYLE_INSTRUCTIONS


def test_language_instructions_completeness():
    """Test all supported languages have instructions."""
    supported_langs = ["en", "zh", "ja", "de", "fr", "ko", "es"]
    for lang in supported_langs:
        assert lang in LANGUAGE_INSTRUCTIONS
