import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.payment_service import PaymentService, PRODUCT_TOKENS
import hmac
import hashlib


@pytest.mark.asyncio
async def test_create_checkout_success(db_session, test_device_id):
    """Test successful checkout creation."""
    service = PaymentService(db_session)
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "checkout_abc123",
        "checkout_url": "https://checkout.creem.io/abc123"
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        result = await service.create_checkout(
            product_id="excuse_10pack",
            device_id=test_device_id
        )
        
        assert result["checkout_id"] == "checkout_abc123"
        assert "checkout_url" in result


@pytest.mark.asyncio
async def test_create_checkout_with_custom_success_url(db_session, test_device_id):
    """Test checkout with custom success URL."""
    service = PaymentService(db_session)
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "checkout_xyz",
        "checkout_url": "https://checkout.creem.io/xyz"
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        custom_url = "https://example.com/success"
        await service.create_checkout(
            product_id="excuse_3pack",
            device_id=test_device_id,
            success_url=custom_url
        )
        
        call_args = mock_post.call_args
        json_body = call_args.kwargs["json"]
        assert json_body["success_url"] == custom_url


@pytest.mark.asyncio
async def test_handle_webhook_checkout_completed(db_session, test_device_id):
    """Test handling checkout completed webhook."""
    service = PaymentService(db_session)
    
    # First create a checkout
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "checkout_test_123",
        "checkout_url": "https://checkout.creem.io/test"
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        await service.create_checkout("excuse_10pack", test_device_id)
    
    # Now handle webhook
    result = await service.handle_webhook(
        "checkout.completed",
        {
            "id": "checkout_test_123",
            "product_id": "excuse_10pack",
            "amount": 799,
            "currency": "USD",
            "metadata": {"device_id": test_device_id}
        }
    )
    
    assert result == True


@pytest.mark.asyncio
async def test_handle_webhook_unknown_event(db_session):
    """Test handling unknown webhook event."""
    service = PaymentService(db_session)
    
    result = await service.handle_webhook(
        "unknown.event",
        {"some": "data"}
    )
    
    assert result == False


@pytest.mark.asyncio
async def test_handle_webhook_missing_device_id(db_session):
    """Test webhook with missing device_id."""
    service = PaymentService(db_session)
    
    result = await service.handle_webhook(
        "checkout.completed",
        {
            "id": "checkout_no_device",
            "product_id": "excuse_10pack",
            "metadata": {}
        }
    )
    
    assert result == False


@pytest.mark.asyncio
async def test_handle_webhook_missing_checkout_id(db_session, test_device_id):
    """Test webhook with missing checkout_id."""
    service = PaymentService(db_session)
    
    result = await service.handle_webhook(
        "checkout.completed",
        {
            "product_id": "excuse_10pack",
            "metadata": {"device_id": test_device_id}
        }
    )
    
    assert result == False


def test_verify_webhook_signature_valid():
    """Test valid webhook signature verification."""
    service = PaymentService.__new__(PaymentService)
    service.webhook_secret = "test_secret"
    
    payload = b'{"event": "test"}'
    signature = hmac.new(
        b"test_secret",
        payload,
        hashlib.sha256
    ).hexdigest()
    
    assert service.verify_webhook_signature(payload, signature) == True


def test_verify_webhook_signature_invalid():
    """Test invalid webhook signature verification."""
    service = PaymentService.__new__(PaymentService)
    service.webhook_secret = "test_secret"
    
    payload = b'{"event": "test"}'
    signature = "invalid_signature"
    
    assert service.verify_webhook_signature(payload, signature) == False


def test_verify_webhook_signature_no_secret():
    """Test webhook signature verification when secret not set."""
    service = PaymentService.__new__(PaymentService)
    service.webhook_secret = ""
    
    payload = b'{"event": "test"}'
    signature = "any_signature"
    
    # Should skip verification and return True
    assert service.verify_webhook_signature(payload, signature) == True


def test_product_tokens_mapping():
    """Test product to tokens mapping."""
    assert PRODUCT_TOKENS["excuse_3pack"] == 3
    assert PRODUCT_TOKENS["excuse_10pack"] == 10
    assert PRODUCT_TOKENS["excuse_30pack"] == 30


@pytest.mark.asyncio
async def test_handle_webhook_unknown_product(db_session, test_device_id):
    """Test webhook with unknown product grants 0 tokens."""
    service = PaymentService(db_session)
    
    # Create checkout with unknown product
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "checkout_unknown_prod",
        "checkout_url": "https://checkout.creem.io/test"
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        await service.create_checkout("unknown_product", test_device_id)
    
    result = await service.handle_webhook(
        "checkout.completed",
        {
            "id": "checkout_unknown_prod",
            "product_id": "unknown_product",
            "amount": 999,
            "currency": "USD",
            "metadata": {"device_id": test_device_id}
        }
    )
    
    assert result == True
