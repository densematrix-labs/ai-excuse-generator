from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import CheckoutRequest, CheckoutResponse
from app.services.payment_service import PaymentService
from typing import Optional

router = APIRouter(prefix="/api/payment", tags=["payment"])


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    request: CheckoutRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a checkout session."""
    payment_service = PaymentService(db)
    try:
        result = await payment_service.create_checkout(
            product_id=request.product_id,
            device_id=request.device_id,
            success_url=request.success_url
        )
        return CheckoutResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkout: {str(e)}")


@router.post("/webhook")
async def handle_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    creem_signature: Optional[str] = Header(None, alias="X-Creem-Signature")
):
    """Handle Creem webhook events."""
    payment_service = PaymentService(db)
    
    body = await request.body()
    
    # Verify signature
    if creem_signature and not payment_service.verify_webhook_signature(body, creem_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    try:
        payload = await request.json()
        event_type = payload.get("event_type", "")
        data = payload.get("data", {})
        
        success = await payment_service.handle_webhook(event_type, data)
        return {"received": True, "processed": success}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")


@router.get("/products")
async def get_products():
    """Get available products."""
    return {
        "products": [
            {
                "id": "excuse_3pack",
                "name": "Starter Pack",
                "description": "3 excuse generations",
                "tokens": 3,
                "price": 2.99,
                "currency": "USD"
            },
            {
                "id": "excuse_10pack",
                "name": "Regular Pack",
                "description": "10 excuse generations",
                "tokens": 10,
                "price": 7.99,
                "currency": "USD"
            },
            {
                "id": "excuse_30pack",
                "name": "Pro Pack",
                "description": "30 excuse generations",
                "tokens": 30,
                "price": 19.99,
                "currency": "USD"
            }
        ]
    }
