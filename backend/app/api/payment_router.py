"""Payment API endpoints (Creem integration)."""
from fastapi import APIRouter, HTTPException, status, Request, Header
from typing import Optional
import hmac
import hashlib

from app.schemas.payment import CheckoutRequest, CheckoutResponse
from app.services.token_service import get_token_service
from app.config import get_settings

router = APIRouter()


# Product configurations
PRODUCTS = {
    "pack_10": {"tokens": 10, "price": 4.99, "name": "10 Excuses Pack"},
    "pack_30": {"tokens": 30, "price": 9.99, "name": "30 Excuses Pack"},
    "unlimited": {"tokens": 0, "price": 14.99, "name": "Unlimited Monthly"},
}


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(request: CheckoutRequest) -> CheckoutResponse:
    """Create a Creem checkout session."""
    settings = get_settings()
    
    if request.product_type not in PRODUCTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid product type: {request.product_type}",
        )
    
    product = PRODUCTS[request.product_type]
    
    # In a real implementation, this would call the Creem API
    # For demo purposes, we return a mock response
    # TODO: Implement actual Creem API call when product IDs are configured
    
    if not settings.creem_api_key:
        # Mock mode - return a test checkout URL
        return CheckoutResponse(
            checkout_url=f"https://checkout.creem.io/test?product={request.product_type}&device={request.device_id}",
            session_id=f"mock_session_{request.device_id}_{request.product_type}",
        )
    
    # Real Creem API call would go here
    # ...
    
    return CheckoutResponse(
        checkout_url="https://checkout.creem.io/...",
        session_id="session_...",
    )


@router.post("/webhook")
async def handle_webhook(
    request: Request,
    x_creem_signature: Optional[str] = Header(None, alias="X-Creem-Signature"),
):
    """Handle Creem webhook for payment completion."""
    settings = get_settings()
    body = await request.body()
    
    # Verify webhook signature if secret is configured
    if settings.creem_webhook_secret and x_creem_signature:
        expected_signature = hmac.new(
            settings.creem_webhook_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        
        if not hmac.compare_digest(expected_signature, x_creem_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature",
            )
    
    payload = await request.json()
    event_type = payload.get("event_type", "")
    data = payload.get("data", {})
    
    if event_type == "checkout.completed":
        device_id = data.get("metadata", {}).get("device_id")
        product_type = data.get("metadata", {}).get("product_type")
        
        if device_id and product_type:
            token_service = get_token_service()
            product = PRODUCTS.get(product_type)
            
            if product:
                if product_type == "unlimited":
                    token_service.set_unlimited(device_id)
                else:
                    token_service.add_tokens(device_id, product["tokens"])
    
    return {"status": "ok"}


@router.get("/products")
async def get_products():
    """Get available products with pricing."""
    return {
        "products": [
            {
                "id": "pack_10",
                "name": "10 Excuses Pack",
                "tokens": 10,
                "price": 4.99,
                "currency": "USD",
                "description": "Perfect for occasional excuse needs",
                "popular": False,
            },
            {
                "id": "pack_30",
                "name": "30 Excuses Pack",
                "tokens": 30,
                "price": 9.99,
                "currency": "USD",
                "description": "Best value for regular users",
                "popular": True,
            },
            {
                "id": "unlimited",
                "name": "Unlimited Monthly",
                "tokens": -1,
                "price": 14.99,
                "currency": "USD",
                "description": "Unlimited excuses for 30 days",
                "popular": False,
            },
        ]
    }
