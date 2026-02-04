import { useState } from "react";
import Swal from "sweetalert2";

export default function ResearchStage({ sessionId, setAgentState }) {
  const [profile, setProfile] = useState({
    name: "",
    job_role: "",
    experience: "",
    skills: ""
  });

  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleProfileChange = (e) =>
    setProfile({ ...profile, [e.target.name]: e.target.value });

  const startAgent = async () => {
    if (!profile.name || !query) {
      Swal.fire("Missing info", "Fill name and research query", "warning");
      return;
    }

    setLoading(true);

    await fetch(`http://localhost:8000/agent/start/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile)
    });

    const res = await fetch(`http://localhost:8000/agent/chat/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query })
    });

    const data = await res.json();
    setAgentState(data);
    localStorage.setItem("candidate_name", data?.candidate_data?.name || "");
    localStorage.setItem("candidate_role", data?.candidate_data?.job_role || "");
    setLoading(false);
  };

  return (
    <div className="card big animate-in">
      <h2 className="card-title">Research & Candidate Profile</h2>

      <div className="form-grid">
        <input name="name" placeholder="Full Name" onChange={handleProfileChange} />
        <input name="job_role" placeholder="Job Role" onChange={handleProfileChange} />
        <input name="experience" placeholder="Experience" onChange={handleProfileChange} />
        <input name="skills" placeholder="Skills" onChange={handleProfileChange} />
      </div>

      <textarea
        className="query"
        placeholder="Enter company / topic to research"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button className="confirm" onClick={startAgent} disabled={loading}>
        {loading ? "Researching..." : "Start"}
      </button>
    </div>
  );
}