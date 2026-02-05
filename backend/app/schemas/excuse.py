from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class Scenario(str, Enum):
    SKIP_WORK = "skip_work"
    AVOID_PARTY = "avoid_party"
    LATE_ARRIVAL = "late_arrival"
    FORGOT_TASK = "forgot_task"
    CANCEL_PLANS = "cancel_plans"
    MISS_MEETING = "miss_meeting"
    CUSTOM = "custom"


class Style(str, Enum):
    SINCERE = "sincere"        # 真诚感人
    PROFESSIONAL = "professional"  # 专业得体
    CREATIVE = "creative"      # 创意独特
    DRAMATIC = "dramatic"      # 夸张戏剧
    ABSURD = "absurd"          # 荒诞搞笑


class ExcuseRequest(BaseModel):
    scenario: Scenario
    custom_scenario: Optional[str] = Field(None, max_length=200)
    style: Style = Style.SINCERE
    target_person: Optional[str] = Field(None, max_length=50)  # boss, friend, family, etc.
    urgency: int = Field(default=3, ge=1, le=5)  # 1-5 urgency level
    device_id: str = Field(..., min_length=10, max_length=100)
    language: str = Field(default="en", pattern="^(en|zh|ja|de|fr|ko|es)$")


class ExcuseResponse(BaseModel):
    excuse: str
    scenario: str
    style: str
    remaining_tokens: int
    is_free_trial: bool = False
