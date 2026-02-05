import pytest
from pydantic import ValidationError
from app.schemas.excuse import ExcuseRequest, ExcuseResponse, Scenario, Style
from app.schemas.payment import CheckoutRequest, CheckoutResponse, TokenStatusResponse


def test_excuse_request_valid():
    """Test valid ExcuseRequest."""
    req = ExcuseRequest(
        scenario=Scenario.SKIP_WORK,
        style=Style.SINCERE,
        device_id="test-device-12345"
    )
    
    assert req.scenario == Scenario.SKIP_WORK
    assert req.style == Style.SINCERE
    assert req.urgency == 3  # default
    assert req.language == "en"  # default


def test_excuse_request_all_fields():
    """Test ExcuseRequest with all fields."""
    req = ExcuseRequest(
        scenario=Scenario.CUSTOM,
        custom_scenario="test scenario",
        style=Style.ABSURD,
        target_person="my boss",
        urgency=5,
        device_id="test-device-12345",
        language="zh"
    )
    
    assert req.custom_scenario == "test scenario"
    assert req.target_person == "my boss"
    assert req.urgency == 5
    assert req.language == "zh"


def test_excuse_request_invalid_device_id_short():
    """Test ExcuseRequest with too short device_id."""
    with pytest.raises(ValidationError):
        ExcuseRequest(
            scenario=Scenario.SKIP_WORK,
            device_id="short"
        )


def test_excuse_request_invalid_urgency():
    """Test ExcuseRequest with invalid urgency."""
    with pytest.raises(ValidationError):
        ExcuseRequest(
            scenario=Scenario.SKIP_WORK,
            device_id="test-device-12345",
            urgency=6
        )


def test_excuse_request_invalid_language():
    """Test ExcuseRequest with invalid language."""
    with pytest.raises(ValidationError):
        ExcuseRequest(
            scenario=Scenario.SKIP_WORK,
            device_id="test-device-12345",
            language="invalid"
        )


def test_excuse_response():
    """Test ExcuseResponse."""
    resp = ExcuseResponse(
        excuse="Test excuse",
        scenario="skip_work",
        style="sincere",
        remaining_tokens=5,
        is_free_trial=True
    )
    
    assert resp.excuse == "Test excuse"
    assert resp.is_free_trial == True


def test_checkout_request_valid():
    """Test valid CheckoutRequest."""
    req = CheckoutRequest(
        product_id="excuse_10pack",
        device_id="test-device-12345"
    )
    
    assert req.product_id == "excuse_10pack"


def test_checkout_request_with_success_url():
    """Test CheckoutRequest with success_url."""
    req = CheckoutRequest(
        product_id="excuse_3pack",
        device_id="test-device-12345",
        success_url="https://example.com/success"
    )
    
    assert req.success_url == "https://example.com/success"


def test_checkout_response():
    """Test CheckoutResponse."""
    resp = CheckoutResponse(
        checkout_url="https://checkout.example.com",
        checkout_id="checkout_123"
    )
    
    assert resp.checkout_url == "https://checkout.example.com"
    assert resp.checkout_id == "checkout_123"


def test_token_status_response():
    """Test TokenStatusResponse."""
    resp = TokenStatusResponse(
        device_id="test-device",
        total_tokens=10,
        used_tokens=3,
        remaining_tokens=7,
        free_trial_available=False
    )
    
    assert resp.remaining_tokens == 7
    assert resp.free_trial_available == False


def test_scenario_enum_values():
    """Test Scenario enum values."""
    assert Scenario.SKIP_WORK.value == "skip_work"
    assert Scenario.AVOID_PARTY.value == "avoid_party"
    assert Scenario.LATE_ARRIVAL.value == "late_arrival"
    assert Scenario.FORGOT_TASK.value == "forgot_task"
    assert Scenario.CANCEL_PLANS.value == "cancel_plans"
    assert Scenario.MISS_MEETING.value == "miss_meeting"
    assert Scenario.CUSTOM.value == "custom"


def test_style_enum_values():
    """Test Style enum values."""
    assert Style.SINCERE.value == "sincere"
    assert Style.PROFESSIONAL.value == "professional"
    assert Style.CREATIVE.value == "creative"
    assert Style.DRAMATIC.value == "dramatic"
    assert Style.ABSURD.value == "absurd"
