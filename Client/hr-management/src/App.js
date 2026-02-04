import { Routes, Route, Navigate } from "react-router-dom";
import CalendarPage from "./pages/Calendar";
import HRApp from "./pages/HRApp";
import Navbar from "./navbar/Navbar";

export default function App() {
  return (
    <>
      <Navbar></Navbar>
      <Routes>
        <Route path="/" element={<Navigate to="/hr" />} />
        <Route path="/hr" element={<HRApp />} />
        <Route path="/calendar" element={<CalendarPage />} />
      </Routes>
    </>
  );
}