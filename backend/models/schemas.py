from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PatientInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str

class BookingRequest(BaseModel):
    appointment_type: str
    date: str
    start_time: str
    patient: PatientInfo
    reason: str

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str
    state: Optional[dict] = None

