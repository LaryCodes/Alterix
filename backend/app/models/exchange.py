from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class ExchangeType(str, Enum):
    DIRECT_SWAP = "DIRECT_SWAP"
    PAID_LEARNING = "PAID_LEARNING"
    MULTI_PARTY_CHAIN = "MULTI_PARTY_CHAIN"


class ExchangeStatus(str, Enum):
    PENDING = "PENDING"
    NEGOTIATING = "NEGOTIATING"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ExchangeBase(BaseModel):
    type: ExchangeType
    status: ExchangeStatus = ExchangeStatus.PENDING


class ExchangeCreate(ExchangeBase):
    participant_ids: List[UUID]
    offerings: dict  # user_id -> skill_id mapping


class Exchange(ExchangeBase):
    id: UUID
    fairness_score: float = 0.0
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ExchangeParticipant(BaseModel):
    id: UUID
    exchange_id: UUID
    user_id: UUID
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExchangeOffering(BaseModel):
    id: UUID
    exchange_id: UUID
    user_id: UUID
    skill_id: UUID
    hours_committed: int = 0
    payment_amount: float = 0.0
    created_at: datetime
    
    class Config:
        from_attributes = True
