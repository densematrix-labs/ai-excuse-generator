from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.excuse import ExcuseRequest, ExcuseResponse
from app.services.excuse_service import ExcuseService
from app.services.token_service import TokenService

router = APIRouter(prefix="/api/excuse", tags=["excuse"])


@router.post("", response_model=ExcuseResponse)
async def generate_excuse(
    request: ExcuseRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate an AI excuse."""
    token_service = TokenService(db)
    
    # Check if can generate
    can_generate, token_type = await token_service.can_generate(request.device_id)
    if not can_generate:
        raise HTTPException(
            status_code=402,
            detail="No tokens available. Please purchase more tokens."
        )
    
    # Generate excuse
    excuse_service = ExcuseService()
    try:
        excuse = await excuse_service.generate_excuse(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate excuse: {str(e)}")
    
    # Consume token
    await token_service.use_token(request.device_id)
    
    # Get updated status
    status = await token_service.get_status(request.device_id)
    
    return ExcuseResponse(
        excuse=excuse,
        scenario=request.scenario.value,
        style=request.style.value,
        remaining_tokens=status["remaining_tokens"],
        is_free_trial=token_type == "free_trial"
    )
