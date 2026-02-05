from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.token import GenerationToken
from typing import Optional


class TokenService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_or_create_token(self, device_id: str) -> GenerationToken:
        """Get token record for device, create if not exists."""
        stmt = select(GenerationToken).where(GenerationToken.device_id == device_id)
        result = await self.db.execute(stmt)
        token = result.scalar_one_or_none()
        
        if not token:
            token = GenerationToken(
                device_id=device_id,
                total_tokens=0,
                used_tokens=0,
                is_free_trial=True,
                free_trial_used=False
            )
            self.db.add(token)
            await self.db.commit()
            await self.db.refresh(token)
        
        return token
    
    async def can_generate(self, device_id: str) -> tuple[bool, str]:
        """Check if device can generate an excuse."""
        token = await self.get_or_create_token(device_id)
        
        # Free trial available
        if token.is_free_trial and not token.free_trial_used:
            return True, "free_trial"
        
        # Has remaining tokens
        if token.remaining_tokens > 0:
            return True, "paid"
        
        return False, "no_tokens"
    
    async def use_token(self, device_id: str) -> bool:
        """Consume one token for generation."""
        token = await self.get_or_create_token(device_id)
        
        # Use free trial
        if token.is_free_trial and not token.free_trial_used:
            token.free_trial_used = True
            await self.db.commit()
            return True
        
        # Use paid token
        if token.remaining_tokens > 0:
            token.used_tokens += 1
            await self.db.commit()
            return True
        
        return False
    
    async def add_tokens(self, device_id: str, amount: int) -> GenerationToken:
        """Add tokens after successful payment."""
        token = await self.get_or_create_token(device_id)
        token.total_tokens += amount
        await self.db.commit()
        await self.db.refresh(token)
        return token
    
    async def get_status(self, device_id: str) -> dict:
        """Get token status for device."""
        token = await self.get_or_create_token(device_id)
        return {
            "device_id": device_id,
            "total_tokens": token.total_tokens,
            "used_tokens": token.used_tokens,
            "remaining_tokens": token.remaining_tokens,
            "free_trial_available": token.is_free_trial and not token.free_trial_used
        }
