from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class GenerationToken(Base):
    __tablename__ = "generation_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(255), index=True, nullable=False)
    total_tokens = Column(Integer, default=0)
    used_tokens = Column(Integer, default=0)
    is_free_trial = Column(Boolean, default=False)
    free_trial_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @property
    def remaining_tokens(self) -> int:
        return self.total_tokens - self.used_tokens
