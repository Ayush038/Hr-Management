import { Routes, Route, Navigate } from "react-router-dom";
import CalendarPage from "./pages/Calendar";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/calendar" />} />
      <Route path="/calendar" element={<CalendarPage />} />
    </Routes>
  );
}
