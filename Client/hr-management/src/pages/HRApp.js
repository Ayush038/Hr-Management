import { useState } from "react";
import Navbar from "../navbar/Navbar";
import StageManager from "../components/StageManager";

export default function HRApp() {
  const [sessionId] = useState(() => "sess_" + Date.now());
  const [agentState, setAgentState] = useState(null);

  return (
    <div className="page">
      <StageManager
        sessionId={sessionId}
        agentState={agentState}
        setAgentState={setAgentState}
      />
    </div>
  );
}