import pytest
from app.models.token import GenerationToken
from app.models.payment import PaymentTransaction


def test_generation_token_remaining_tokens():
    """Test GenerationToken remaining_tokens property."""
    token = GenerationToken(
        device_id="test-device",
        total_tokens=10,
        used_tokens=3
    )
    
    assert token.remaining_tokens == 7


def test_generation_token_remaining_tokens_zero():
    """Test remaining_tokens when all used."""
    token = GenerationToken(
        device_id="test-device",
        total_tokens=5,
        used_tokens=5
    )
    
    assert token.remaining_tokens == 0


def test_generation_token_defaults():
    """Test GenerationToken default values."""
    token = GenerationToken(device_id="test")
    
    assert token.total_tokens == 0
    assert token.used_tokens == 0
    assert token.is_free_trial == False
    assert token.free_trial_used == False


def test_payment_transaction_defaults():
    """Test PaymentTransaction default values."""
    tx = PaymentTransaction(
        checkout_id="checkout_123",
        device_id="device_123"
    )
    
    assert tx.status == "pending"
    assert tx.tokens_granted == 0
