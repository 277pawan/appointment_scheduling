from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Use relative imports or sys.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.api.chat import router as chat_router
from backend.api.calendly_integration import router as calendly_router

app = FastAPI(title="Medical Appointment Scheduling Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(calendly_router, prefix="/api/calendly", tags=["calendly"])

@app.get("/health")
async def health():
    return {"status": "ok"}

