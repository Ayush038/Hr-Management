import { API_BASE } from "../config/api";
import { useState, useEffect } from "react";
import BookingModal from "../components/BookingModal";

export default function CalendarPage() {
  const [selectedDate, setSelectedDate] = useState(null);
  const [month, setMonth] = useState(1);
  const [bookedSlots, setBookedSlots] = useState([]);

  const [lockedName] = useState(
    () => localStorage.getItem("candidate_name") || ""
  );

  const year = 2026;
  const monthNames = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
  ];

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  const goPrev = () => setMonth((m) => (m === 0 ? 11 : m - 1));
  const goNext = () => setMonth((m) => (m === 11 ? 0 : m + 1));

  useEffect(() => {
    if (!selectedDate) return;

    fetch(`${API_BASE}/api/bookings/${selectedDate}`)
      .then(res => res.json())
      .then(data => setBookedSlots(data));
  }, [selectedDate]);

  return (
    <div className="calendar-page">
      <div className="page">
        <div className="card big">
          <div className="header">
            <button className="nav" onClick={goPrev}>‹</button>
            <h2 className="title">{monthNames[month]} {year}</h2>
            <button className="nav" onClick={goNext}>›</button>
          </div>

          <div className="grid large">
            {days.map((d) => {
              const date = `${year}-${String(month+1).padStart(2,"0")}-${String(d).padStart(2,"0")}`;
              return (
                <button
                  key={date}
                  id={`date-${date}`}
                  className="day"
                  onClick={() => setSelectedDate(date)}
                >
                  {d}
                </button>
              );
            })}
          </div>
        </div>

        {selectedDate && (
          <BookingModal
            date={selectedDate}
            bookedSlots={bookedSlots}
            candidateName={lockedName}   // ✅ always from storage
            onClose={() => setSelectedDate(null)}
            onBooked={() => {
              fetch(`${API_BASE}/api/bookings/${selectedDate}`)
                .then(res => res.json())
                .then(data => setBookedSlots(data));
            }}
          />
        )}
      </div>
    </div>
  );
}