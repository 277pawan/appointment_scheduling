from fastapi import APIRouter
from backend.models.schemas import ChatRequest, ChatResponse
from backend.agent.scheduling_agent import handle_chat

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    return await handle_chat(payload)

