from fastapi import APIRouter
from services.computer_service import click_calendar

router = APIRouter(prefix="/computer", tags=["Computer Use"])

@router.post("/click")
def click(data: dict):
    try:
        return click_calendar(data)
    except Exception as e:
        return {"status": "error", "message": str(e)}