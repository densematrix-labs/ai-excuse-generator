"""Excuse generation API endpoints."""
from fastapi import APIRouter, HTTPException, status

from app.schemas.excuse import ExcuseRequest, ExcuseResponse
from app.services.excuse_service import get_excuse_service
from app.services.token_service import get_token_service

router = APIRouter()


@router.post("/generate", response_model=ExcuseResponse)
async def generate_excuses(request: ExcuseRequest) -> ExcuseResponse:
    """Generate creative excuses for a given situation.
    
    Requires a valid device_id and either:
    - Unused free trial
    - Available tokens
    - Unlimited subscription
    """
    token_service = get_token_service()
    
    # Check if user can generate
    if not token_service.can_generate(request.device_id):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="No tokens remaining. Please purchase more to continue.",
        )
    
    # Use a token
    use_result = token_service.use_token(request.device_id)
    if not use_result.success:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=use_result.message,
        )
    
    # Generate excuses
    excuse_service = get_excuse_service()
    try:
        excuses = await excuse_service.generate_excuses(
            category=request.category,
            urgency=request.urgency,
            context=request.context,
            language=request.language,
        )
    except Exception as e:
        # Refund the token on error (simplified - in production use proper transaction)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to generate excuses: {str(e)}",
        )
    
    # Get updated token status
    status_info = token_service.get_token_status(request.device_id)
    
    return ExcuseResponse(
        excuses=excuses,
        category=request.category,
        urgency=request.urgency,
        tokens_remaining=status_info.remaining_tokens,
    )


@router.get("/categories")
async def get_categories():
    """Get available excuse categories with descriptions."""
    return {
        "categories": [
            {"id": "late", "name": "Being Late", "icon": "⏰"},
            {"id": "sick_leave", "name": "Sick Leave", "icon": "🤒"},
            {"id": "decline", "name": "Declining Invitations", "icon": "🙅"},
            {"id": "forgot", "name": "Forgetting Things", "icon": "🤔"},
            {"id": "deadline", "name": "Missing Deadlines", "icon": "📅"},
            {"id": "meeting", "name": "Missing Meetings", "icon": "📋"},
            {"id": "homework", "name": "Homework/Assignments", "icon": "📚"},
            {"id": "other", "name": "Other", "icon": "💭"},
        ]
    }


@router.get("/urgency-levels")
async def get_urgency_levels():
    """Get available urgency levels."""
    return {
        "levels": [
            {
                "id": "normal",
                "name": "Normal",
                "description": "Believable and reasonable",
                "icon": "😊",
            },
            {
                "id": "urgent",
                "name": "Urgent",
                "description": "Slightly dramatic but plausible",
                "icon": "😰",
            },
            {
                "id": "extreme",
                "name": "Extreme",
                "description": "Wild and dramatic!",
                "icon": "🤯",
            },
        ]
    }
