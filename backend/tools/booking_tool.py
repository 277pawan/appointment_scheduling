import httpx
import os
from models.schemas import BookingRequest

BACKEND_BASE = os.getenv("BACKEND_BASE", "http://localhost:8000")

async def book_slot(payload: BookingRequest):
    url = f"{BACKEND_BASE}/api/calendly/book"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict())
        resp.raise_for_status()
        return resp.json()

