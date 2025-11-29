import httpx
import os

BACKEND_BASE = os.getenv("BACKEND_BASE", "http://localhost:8000")

async def get_available_slots(date: str, appointment_type: str):
    url = f"{BACKEND_BASE}/api/calendly/availability"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={"date": date, "appointment_type": appointment_type})
        resp.raise_for_status()
        return resp.json()

