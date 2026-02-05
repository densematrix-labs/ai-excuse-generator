import pytest
from app.services.token_service import TokenService


@pytest.mark.asyncio
async def test_get_or_create_token_new_device(db_session, test_device_id):
    """Test creating new token record for new device."""
    service = TokenService(db_session)
    token = await service.get_or_create_token(test_device_id)
    
    assert token.device_id == test_device_id
    assert token.total_tokens == 0
    assert token.used_tokens == 0
    assert token.is_free_trial == True
    assert token.free_trial_used == False


@pytest.mark.asyncio
async def test_get_or_create_token_existing_device(db_session, test_device_id):
    """Test getting existing token record."""
    service = TokenService(db_session)
    
    # Create first
    token1 = await service.get_or_create_token(test_device_id)
    # Get again
    token2 = await service.get_or_create_token(test_device_id)
    
    assert token1.id == token2.id


@pytest.mark.asyncio
async def test_can_generate_free_trial(db_session, test_device_id):
    """Test free trial availability."""
    service = TokenService(db_session)
    
    can_gen, token_type = await service.can_generate(test_device_id)
    
    assert can_gen == True
    assert token_type == "free_trial"


@pytest.mark.asyncio
async def test_can_generate_no_tokens(db_session, test_device_id):
    """Test when no tokens available."""
    service = TokenService(db_session)
    
    # Use free trial
    await service.use_token(test_device_id)
    
    can_gen, token_type = await service.can_generate(test_device_id)
    
    assert can_gen == False
    assert token_type == "no_tokens"


@pytest.mark.asyncio
async def test_can_generate_paid_tokens(db_session, test_device_id):
    """Test with paid tokens."""
    service = TokenService(db_session)
    
    # Use free trial
    await service.use_token(test_device_id)
    # Add paid tokens
    await service.add_tokens(test_device_id, 5)
    
    can_gen, token_type = await service.can_generate(test_device_id)
    
    assert can_gen == True
    assert token_type == "paid"


@pytest.mark.asyncio
async def test_use_token_free_trial(db_session, test_device_id):
    """Test using free trial token."""
    service = TokenService(db_session)
    
    result = await service.use_token(test_device_id)
    token = await service.get_or_create_token(test_device_id)
    
    assert result == True
    assert token.free_trial_used == True


@pytest.mark.asyncio
async def test_use_token_paid(db_session, test_device_id):
    """Test using paid token."""
    service = TokenService(db_session)
    
    # Use free trial first
    await service.use_token(test_device_id)
    # Add tokens
    await service.add_tokens(test_device_id, 3)
    # Use paid token
    result = await service.use_token(test_device_id)
    
    token = await service.get_or_create_token(test_device_id)
    
    assert result == True
    assert token.used_tokens == 1


@pytest.mark.asyncio
async def test_use_token_no_tokens(db_session, test_device_id):
    """Test using token when none available."""
    service = TokenService(db_session)
    
    # Use free trial
    await service.use_token(test_device_id)
    # Try to use when no tokens
    result = await service.use_token(test_device_id)
    
    assert result == False


@pytest.mark.asyncio
async def test_add_tokens(db_session, test_device_id):
    """Test adding tokens."""
    service = TokenService(db_session)
    
    token = await service.add_tokens(test_device_id, 10)
    
    assert token.total_tokens == 10
    assert token.remaining_tokens == 10


@pytest.mark.asyncio
async def test_get_status(db_session, test_device_id):
    """Test getting token status."""
    service = TokenService(db_session)
    
    await service.add_tokens(test_device_id, 5)
    await service.use_token(test_device_id)  # uses free trial
    
    status = await service.get_status(test_device_id)
    
    assert status["device_id"] == test_device_id
    assert status["total_tokens"] == 5
    assert status["used_tokens"] == 0
    assert status["remaining_tokens"] == 5
    assert status["free_trial_available"] == False


@pytest.mark.asyncio
async def test_remaining_tokens_property(db_session, test_device_id):
    """Test remaining_tokens property."""
    service = TokenService(db_session)
    
    token = await service.add_tokens(test_device_id, 10)
    # Use free trial first
    await service.use_token(test_device_id)
    # Use 3 paid tokens
    for _ in range(3):
        await service.use_token(test_device_id)
    
    token = await service.get_or_create_token(test_device_id)
    assert token.remaining_tokens == 7
