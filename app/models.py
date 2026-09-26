from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class BookingCreate(BaseModel):
    patient_name: str = Field(min_length=1, max_length=100)
    doctor_id: str = Field(min_length=1)
    slot: datetime


class BookingResponse(BaseModel):
    id: str
    patient_name: str
    doctor_id: str
    slot: datetime
    status: BookingStatus
    created_at: datetime
