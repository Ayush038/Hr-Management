import { useState } from "react";
import Swal from "sweetalert2";

export default function ScheduleStage({ agentState, setAgentState }) {
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [sending, setSending] = useState(false);

  const to12Hour = (time24) => {
    let [h, m] = time24.split(":").map(Number);
    const ampm = h >= 12 ? "PM" : "AM";
    h = h % 12 || 12;
    return `${h} ${ampm}`;
  };

  const submit = async () => {
    if (!date || !time) {
      Swal.fire("Missing info", "Pick a date and time", "warning");
      return;
    }

    const formattedTime = to12Hour(time);
    const sentence = `I am free on ${date} at ${formattedTime}`;

    setSending(true);

    try {
      const res = await fetch(
        `http://localhost:8000/agent/chat/${agentState.session_id}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: sentence,
            force_step: "scheduling"
          })
        }
      );

      const data = await res.json();
      setAgentState(data);
    } catch (err) {
      Swal.fire("Error", "Backend not reachable", "error");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="card big animate-in center-card schedule-card">
      <h2 className="card-title">📅 Select your ⌚ Availability</h2>
      <p className="subtext">Choose a date and time for your interview</p>

      <div className="schedule-grid align">
        <div className="schedule-field">
          <label>Date</label>
          <input
            type="date"
            className="schedule-input"
            min={new Date().toISOString().split("T")[0]}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="schedule-field">
          <label>Time (9 AM – 5 PM)</label>
          <select
            className="schedule-input"
            onChange={(e) => setTime(e.target.value)}
          >
            <option value="">Select time</option>
            <option value="09:00">9:00 AM</option>
            <option value="10:00">10:00 AM</option>
            <option value="11:00">11:00 AM</option>
            <option value="12:00">12:00 PM</option>
            <option value="13:00">1:00 PM</option>
            <option value="14:00">2:00 PM</option>
            <option value="15:00">3:00 PM</option>
            <option value="16:00">4:00 PM</option>
            <option value="17:00">5:00 PM</option>
          </select>
        </div>
      </div>

      <button className="confirm" onClick={submit} disabled={sending}>
        {sending ? "Scheduling..." : "Confirm Slot"}
      </button>
    </div>
  );
}