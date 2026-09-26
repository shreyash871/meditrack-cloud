from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.core.database import get_database
from app.models import BookingCreate, BookingResponse, BookingStatus

router = APIRouter(prefix="/bookings", tags=["bookings"])


def _serialize(doc) -> BookingResponse:
    return BookingResponse(
        id=str(doc["_id"]),
        patient_name=doc["patient_name"],
        doctor_id=doc["doctor_id"],
        slot=doc["slot"],
        status=doc["status"],
        created_at=doc["created_at"],
    )


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(payload: BookingCreate):
    db = get_database()
    doc = {
        "patient_name": payload.patient_name,
        "doctor_id": payload.doctor_id,
        "slot": payload.slot,
        "status": BookingStatus.CONFIRMED.value,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        result = await db.bookings.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already booked for that slot",
        )
    doc["_id"] = result.inserted_id
    return _serialize(doc)


@router.get("", response_model=list[BookingResponse])
async def list_bookings():
    db = get_database()
    docs = await db.bookings.find().sort("slot", 1).to_list(length=100)
    return [_serialize(d) for d in docs]


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str):
    db = get_database()
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking id")
    doc = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Booking not found")
    return _serialize(doc)
