from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class CheckoutRequest(BaseModel):
    product_id: str
    device_id: str = Field(..., min_length=10, max_length=100)
    success_url: Optional[str] = None
    

class CheckoutResponse(BaseModel):
    checkout_url: str
    checkout_id: str


class TokenStatusResponse(BaseModel):
    device_id: str
    total_tokens: int
    used_tokens: int
    remaining_tokens: int
    free_trial_available: bool


class WebhookPayload(BaseModel):
    event_type: str
    data: Dict[str, Any]
