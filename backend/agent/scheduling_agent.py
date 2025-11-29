from typing import Dict, Any
from models.schemas import ChatRequest, ChatResponse, BookingRequest, PatientInfo
from rag.faq_rag import answer_faq
from tools.availability_tool import get_available_slots
from tools.booking_tool import book_slot

# Very simple “state machine” kept in memory per conversation id if needed.
# For assessment, keep it stateless and let frontend store context.

async def handle_chat(req: ChatRequest) -> ChatResponse:
    # take latest user message
    user_msg = next((m for m in reversed(req.messages) if m.role == "user"), None)
    if not user_msg:
        return ChatResponse(reply="How can I help you today?")

    text = user_msg.content.lower()

    # detect FAQ vs scheduling in a very naive way
    if any(k in text for k in ["insurance", "parking", "hours", "location", "billing", "cancel policy", "covid"]):
        answer = answer_faq(user_msg.content)
        # simple hint to continue scheduling
        reply = f"{answer}\n\nIf you’d like, we can continue scheduling your appointment now."
        return ChatResponse(reply=reply)

    # scheduling flow examples (simplified)
    if "book" in text or "appointment" in text or "schedule" in text:
        reply = (
            "I can help you schedule an appointment.\n"
            "What is the main reason for your visit (e.g., headaches, follow‑up, physical exam)?"
        )
        return ChatResponse(reply=reply)

    if "headache" in text or "checkup" in text or "consultation" in text:
        reply = (
            "For that, a general consultation (30 minutes) is usually appropriate.\n"
            "Do you prefer morning or afternoon, and on which date?"
        )
        return ChatResponse(reply=reply)

    if "tomorrow" in text or "this week" in text:
        # for demo, just call availability for tomorrow with consultation
        # in real version you should parse date/time
        from datetime import datetime, timedelta
        target_date = (datetime.now() + timedelta(days=1)).date().isoformat()
        slots = await get_available_slots(target_date, "consultation")
        available = [s for s in slots["available_slots"] if s["available"]][:5]
        if not available:
            reply = "There are no available slots tomorrow. Would you like another date?"
        else:
            lines = [f"- {target_date} at {s['start_time']}" for s in available]
            reply = "Here are some available options:\n" + "\n".join(lines) + "\nWhich one works for you?"
        return ChatResponse(reply=reply, state={"suggested_date": target_date, "type": "consultation"})

    # final: ask for clarification
    return ChatResponse(
        reply="To help you better, tell me if you want to book, reschedule, cancel, or ask about the clinic."
    )

