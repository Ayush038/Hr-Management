from fastapi import APIRouter, Body
from services.chat_services import process_message, init_session

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/start/{session_id}")
def start(session_id: str, data: dict = Body(...)):
    return init_session(session_id, data)

@router.post("/chat/{session_id}")
def chat(session_id: str, data: dict = Body(...)):
    message = data.get("message")
    return process_message(session_id, message)