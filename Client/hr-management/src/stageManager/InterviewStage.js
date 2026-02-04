import { API_BASE } from "../config/api";
import { useState, useEffect, useRef } from "react";

export default function InterviewStage({ sessionId, agentState, setAgentState }) {
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  const [lockedSummary, setLockedSummary] = useState(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [agentState, sending]);

  useEffect(() => {
    if (!lockedSummary && agentState?.candidate_data?.research_summary) {
      setLockedSummary(agentState.candidate_data.research_summary);
    }
  }, [agentState, lockedSummary]);

  const send = async () => {
    if (!input.trim()) return;
    setSending(true);

    const res = await fetch(`${API_BASE}/agent/chat/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });

    const data = await res.json();
    setAgentState(data);
    setInput("");
    setSending(false);
  };

  const copyText = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error("Copy failed", err);
    }
  };

  return (
    <div
      className={`interview-layout ${
        agentState?.current_step === "end" ? "slide-out" : "animate-in"
      }`}
    >
      <div className="card chat-card fixed-chat">
        <h3 className="chat-title">Interview</h3>

        <div className="chat-box fixed">
          {(agentState?.messages || []).map((m, i) => (
            <div
              key={i}
              className={`chat-message ${m.role === "user" ? "user" : "ai"}`}
            >
              <div className="bubble">
                {m.content}

                {m.role !== "user" && (
                  <button
                    className="copy-btn"
                    onClick={() => copyText(m.content)}
                    title="Copy"
                  >
                    📋
                  </button>
                )}
              </div>
            </div>
          ))}

          {sending && (
            <div className="chat-message ai">
              <div className="thinking">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <div className="input-row">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer..."
            onKeyDown={(e) => e.key === "Enter" && send()}
            disabled={sending}
          />
          <button onClick={send} disabled={sending}>
            Send
          </button>
        </div>
      </div>

      <div className="card side-card">
        <h3>Research Summary</h3>
        <p>{lockedSummary || "Loading..."}</p>
      </div>
    </div>
  );
}