from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import TokenStatusResponse
from app.services.token_service import TokenService

router = APIRouter(prefix="/api/tokens", tags=["tokens"])


@router.get("/{device_id}", response_model=TokenStatusResponse)
async def get_token_status(
    device_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get token status for a device."""
    token_service = TokenService(db)
    status = await token_service.get_status(device_id)
    return TokenStatusResponse(**status)
