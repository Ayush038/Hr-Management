import { useState, useEffect, useRef } from "react";

export default function InterviewStage({ sessionId, agentState, setAgentState }) {
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [agentState]);

  const send = async () => {
    if (!input.trim()) return;
    setSending(true);

    const res = await fetch(`http://localhost:8000/agent/chat/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();
    setAgentState(data);
    setInput("");
    setSending(false);
  };

  return (
    <div className={`interview-layout ${agentState?.current_step === "end" ? "slide-out" : "animate-in"}`}>
      <div className="card chat-card">
        <h3>Interview</h3>

        <div className="chat-box">
          {(agentState?.messages || []).map((m, i) => (
            <div key={i} className={`bubble ${m.role}`}>
              {m.content}
            </div>
          ))}

          {sending && <div className="typing">HR Agent is typing...</div>}
          <div ref={bottomRef} />
        </div>

        <div className="input-row">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer..."
            onKeyDown={(e) => e.key === "Enter" && send()}
          />
          <button onClick={send} disabled={sending}>
            Send
          </button>
        </div>
      </div>

      <div className="card side-card">
        <h3>Research Summary</h3>
        <p>{agentState?.candidate_data?.research_summary || "Loading..."}</p>
      </div>
    </div>
  );
}