import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ai-excuse-generator"


@pytest.mark.asyncio
async def test_root(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Excuse Generator"
    assert "version" in data


@pytest.mark.asyncio
async def test_get_token_status(client, test_device_id):
    """Test token status endpoint."""
    response = await client.get(f"/api/tokens/{test_device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == test_device_id
    assert data["free_trial_available"] == True


@pytest.mark.asyncio
async def test_generate_excuse_success(client, test_device_id):
    """Test excuse generation endpoint."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "My goldfish needed emergency therapy."}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await client.post("/api/excuse", json={
            "scenario": "skip_work",
            "style": "absurd",
            "device_id": test_device_id,
            "language": "en"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["excuse"] == "My goldfish needed emergency therapy."
        assert data["scenario"] == "skip_work"
        assert data["style"] == "absurd"
        assert data["is_free_trial"] == True


@pytest.mark.asyncio
async def test_generate_excuse_no_tokens(client, test_device_id):
    """Test excuse generation when no tokens available."""
    # First use free trial
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "First excuse"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        # Use free trial
        await client.post("/api/excuse", json={
            "scenario": "skip_work",
            "style": "sincere",
            "device_id": test_device_id
        })
        
        # Try again without tokens
        response = await client.post("/api/excuse", json={
            "scenario": "skip_work",
            "style": "sincere",
            "device_id": test_device_id
        })
        
        assert response.status_code == 402
        assert "No tokens" in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_excuse_invalid_scenario(client, test_device_id):
    """Test excuse generation with invalid scenario."""
    response = await client.post("/api/excuse", json={
        "scenario": "invalid_scenario",
        "style": "sincere",
        "device_id": test_device_id
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_excuse_invalid_style(client, test_device_id):
    """Test excuse generation with invalid style."""
    response = await client.post("/api/excuse", json={
        "scenario": "skip_work",
        "style": "invalid_style",
        "device_id": test_device_id
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_excuse_invalid_language(client, test_device_id):
    """Test excuse generation with invalid language."""
    response = await client.post("/api/excuse", json={
        "scenario": "skip_work",
        "style": "sincere",
        "device_id": test_device_id,
        "language": "invalid"
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_excuse_custom_scenario(client, test_device_id):
    """Test excuse generation with custom scenario."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Custom scenario excuse."}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await client.post("/api/excuse", json={
            "scenario": "custom",
            "custom_scenario": "need to skip gym today",
            "style": "creative",
            "device_id": test_device_id
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["excuse"] == "Custom scenario excuse."


@pytest.mark.asyncio
async def test_get_products(client):
    """Test products endpoint."""
    response = await client.get("/api/payment/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 3
    
    product_ids = [p["id"] for p in data["products"]]
    assert "excuse_3pack" in product_ids
    assert "excuse_10pack" in product_ids
    assert "excuse_30pack" in product_ids


@pytest.mark.asyncio
async def test_webhook_invalid_payload(client):
    """Test webhook with invalid payload."""
    response = await client.post("/api/payment/webhook", content="invalid json")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_webhook_checkout_completed(client, test_device_id):
    """Test webhook checkout completed event."""
    payload = {
        "event_type": "checkout.completed",
        "data": {
            "id": "checkout_123",
            "product_id": "excuse_10pack",
            "amount": 799,
            "currency": "USD",
            "metadata": {
                "device_id": test_device_id
            }
        }
    }
    
    response = await client.post("/api/payment/webhook", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["received"] == True


@pytest.mark.asyncio 
async def test_generate_excuse_llm_error(client, test_device_id):
    """Test excuse generation when LLM fails."""
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = Exception("LLM service unavailable")
        
        response = await client.post("/api/excuse", json={
            "scenario": "skip_work",
            "style": "sincere",
            "device_id": test_device_id
        })
        
        assert response.status_code == 500
        assert "Failed to generate" in response.json()["detail"]
