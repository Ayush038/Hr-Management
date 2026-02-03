from fastapi import APIRouter
from tools.booking import save_booking, get_bookings_by_date

router = APIRouter(prefix="/api", tags=["Calendar"])

@router.get("/bookings/{date}")
def fetch_bookings(date: str):
    return get_bookings_by_date(date)

@router.post("/book")
def book_slot(data: dict):
    save_booking(
        name=data["name"],
        date=data["date"],
        time=data["time"]
    )
    return {"status": "booked"}