import Swal from "sweetalert2";

const SLOTS = [9, 10, 11, 12, 14, 15, 16, 17];

export default function BookingModal({ date, bookedSlots, onClose, onBooked }) {
  const name = "John Doe";

  const handleClick = async (hour) => {
    await fetch("http://localhost:8000/api/book", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        date,
        time: String(hour).padStart(2, "0") + ":00"
      })
    });

    onClose();
    onBooked();

    Swal.fire({
      title: "Booked!",
      text: `Slot ${hour}:00 on ${date} is confirmed.`,
      icon: "success",
      background: "linear-gradient(135deg, rgba(30,41,59,.9), rgba(2,6,23,.95))",
      color: "#e5e7eb",
      backdrop: "rgba(2,6,23,.75)",
      confirmButtonText: "Nice",
      confirmButtonColor: "#38bdf8",
      customClass: {
        popup: "glass-swal"
      }
    });
  };

  return (
    <div className="overlay">
      <div className="modal">
        <h3>Select time for {date}</h3>

        <div className="modal-body">
          <div className="slots">
            {SLOTS.map((h) => {
              const id = `slot-${date}-${h}`;
              const isBooked = bookedSlots.some(b => b.time === `${String(h).padStart(2,"0")}:00`);

              return (
                <button
                  key={id}
                  id={id}
                  className={`slot ${isBooked ? "booked" : ""}`}
                  disabled={isBooked}
                  onClick={() => !isBooked && handleClick(h)}
                >
                  {h}:00
                </button>
              );
            })}
          </div>

          <div className="panel">
            <h4>Booked</h4>
            {bookedSlots.map((b, i) => (
              <div key={i}>{b.time} — {b.name}</div>
            ))}
          </div>
        </div>

        <button className="close" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}