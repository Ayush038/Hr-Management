import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const nav = useNavigate();

  return (
    <div className="navbar">
      <h2 className="brand">HR-Management System</h2>
      <button className="nav-btn" onClick={() => nav("/calendar")}>
        Calendar
      </button>
    </div>
  );
}