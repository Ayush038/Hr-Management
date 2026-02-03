from datetime import datetime
from db import db

def save_booking(name: str, date: str, time: str):
    db.bookings.insert_one({
        "name": name,
        "date": date,
        "time": time,
        "timestamp": datetime.utcnow()
    })

def get_bookings_by_date(date: str):
    return list(db.bookings.find(
        {"date": date},
        {"_id": 0}
    ))