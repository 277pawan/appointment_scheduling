from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from models.schemas import BookingRequest, BookingResponse
from datetime import datetime, timedelta

router = APIRouter()

# In-memory mock store
MOCK_BOOKINGS: List[Dict[str, Any]] = []

APPOINTMENT_DURATIONS = {
    "consultation": 30,
    "followup": 15,
    "physical": 45,
    "special": 60,
}

@router.get("/availability")
def get_availability(
    date: str = Query(...),
    appointment_type: str = Query(...)
):
    # parse date
    try:
        day = datetime.fromisoformat(date).date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    duration = APPOINTMENT_DURATIONS.get(appointment_type, 30)

    # simple mock: working hours 09:00–17:00
    slots = []
    current = datetime.combine(day, datetime.min.time()).replace(hour=9, minute=0)
    end = current.replace(hour=17, minute=0)

    while current + timedelta(minutes=duration) <= end:
        start_str = current.strftime("%H:%M")
        end_str = (current + timedelta(minutes=duration)).strftime("%H:%M")
        # check booking conflict
        available = True
        for b in MOCK_BOOKINGS:
            if b["date"] == date and b["start_time"] == start_str:
                available = False
                break
        slots.append(
            {
                "start_time": start_str,
                "end_time": end_str,
                "available": available,
            }
        )
        current += timedelta(minutes=duration)

    return {
        "date": date,
        "available_slots": slots,
    }

@router.post("/book", response_model=BookingResponse)
def book_appointment(payload: BookingRequest):
    # check if slot already booked
    for b in MOCK_BOOKINGS:
        if b["date"] == payload.date and b["start_time"] == payload.start_time:
            raise HTTPException(status_code=409, detail="Slot already booked")

    booking_id = f"APPT-{len(MOCK_BOOKINGS)+1:04d}"
    confirmation_code = f"CONF-{len(MOCK_BOOKINGS)+1:04d}"

    record = {
        "booking_id": booking_id,
        "confirmation_code": confirmation_code,
        "appointment_type": payload.appointment_type,
        "date": payload.date,
        "start_time": payload.start_time,
        "patient": payload.patient.dict(),
        "reason": payload.reason,
        "status": "confirmed",
    }
    MOCK_BOOKINGS.append(record)

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        confirmation_code=confirmation_code,
        details=record,
    )

