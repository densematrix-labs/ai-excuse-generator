"""Excuse-related schemas."""
from pydantic import BaseModel, Field
from typing import List, Literal
from enum import Enum


class ExcuseCategory(str, Enum):
    """Available excuse categories."""
    LATE = "late"                    # 迟到
    SICK_LEAVE = "sick_leave"        # 请病假
    DECLINE = "decline"              # 拒绝邀请
    FORGOT = "forgot"                # 忘事
    DEADLINE = "deadline"            # 错过截止日期
    MEETING = "meeting"              # 缺席会议
    HOMEWORK = "homework"            # 没完成作业
    OTHER = "other"                  # 其他


class UrgencyLevel(str, Enum):
    """Urgency/believability level."""
    NORMAL = "normal"      # 常规借口，比较可信
    URGENT = "urgent"      # 紧急借口，有点夸张
    EXTREME = "extreme"    # 极端借口，非常戏剧化


class ExcuseRequest(BaseModel):
    """Request body for generating excuses."""
    category: ExcuseCategory = Field(..., description="The excuse category")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.NORMAL, description="Urgency level")
    context: str = Field(default="", max_length=500, description="Additional context")
    language: str = Field(default="en", description="Output language code")
    device_id: str = Field(..., min_length=10, max_length=100, description="Device fingerprint")


class Excuse(BaseModel):
    """A single generated excuse."""
    text: str = Field(..., description="The excuse text")
    tone: str = Field(..., description="The tone of the excuse")
    tip: str = Field(default="", description="Delivery tip")


class ExcuseResponse(BaseModel):
    """Response containing generated excuses."""
    excuses: List[Excuse] = Field(..., description="List of generated excuses")
    category: ExcuseCategory
    urgency: UrgencyLevel
    tokens_remaining: int = Field(default=-1, description="Remaining tokens, -1 if unlimited or unknown")
