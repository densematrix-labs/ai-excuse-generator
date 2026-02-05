import httpx
import hmac
import hashlib
import json
from app.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.payment import PaymentTransaction
from app.services.token_service import TokenService
from datetime import datetime

settings = get_settings()

# Product configurations: product_id -> tokens
PRODUCT_TOKENS = {
    "excuse_3pack": 3,
    "excuse_10pack": 10,
    "excuse_30pack": 30,
}


class PaymentService:
    CREEM_API_URL = "https://api.creem.io/v1"
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.api_key = settings.creem_api_key
        self.webhook_secret = settings.creem_webhook_secret
    
    async def create_checkout(
        self, 
        product_id: str, 
        device_id: str,
        success_url: str = None
    ) -> dict:
        """Create a Creem checkout session."""
        if not success_url:
            success_url = "https://excuse.demo.densematrix.ai/payment/success"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.CREEM_API_URL}/checkouts",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "product_id": product_id,
                    "success_url": success_url,
                    "metadata": {
                        "device_id": device_id
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Record transaction
        transaction = PaymentTransaction(
            checkout_id=data["id"],
            device_id=device_id,
            product_id=product_id,
            status="pending"
        )
        self.db.add(transaction)
        await self.db.commit()
        
        return {
            "checkout_url": data["checkout_url"],
            "checkout_id": data["id"]
        }
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Creem webhook signature."""
        if not self.webhook_secret:
            return True  # Skip verification in dev
        
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)
    
    async def handle_webhook(self, event_type: str, data: dict) -> bool:
        """Handle Creem webhook events."""
        if event_type == "checkout.completed":
            checkout_id = data.get("id")
            metadata = data.get("metadata", {})
            device_id = metadata.get("device_id")
            product_id = data.get("product_id")
            
            if not device_id or not checkout_id:
                return False
            
            # Update transaction
            stmt = select(PaymentTransaction).where(
                PaymentTransaction.checkout_id == checkout_id
            )
            result = await self.db.execute(stmt)
            transaction = result.scalar_one_or_none()
            
            if transaction:
                transaction.status = "completed"
                transaction.completed_at = datetime.utcnow()
                transaction.amount = data.get("amount", 0) / 100  # cents to dollars
                transaction.currency = data.get("currency", "USD")
                
                # Grant tokens
                tokens = PRODUCT_TOKENS.get(product_id, 0)
                if tokens > 0:
                    token_service = TokenService(self.db)
                    await token_service.add_tokens(device_id, tokens)
                    transaction.tokens_granted = tokens
                
                await self.db.commit()
                return True
        
        return False
