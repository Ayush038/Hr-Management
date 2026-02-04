import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const nav = useNavigate();

  return (
    <div className="navbar">
      <div
        className="nav-left"
        onClick={() => nav("/")}
        style={{ cursor: "pointer" }}
      >
        <img src="Logo.png" alt="Logo" className="logo" />
        <h2 className="brand">HR-Management System</h2>
      </div>

      <button className="nav-btn" onClick={() => nav("/calendar")}>
        <img src="calendar.png" alt="Calendar" className="icon" />
      </button>
    </div>
  );
}
