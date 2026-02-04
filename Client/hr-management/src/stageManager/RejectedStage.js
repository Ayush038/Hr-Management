import { useNavigate } from "react-router-dom";

export default function EndStage({ agentState }) {
  const nav = useNavigate();

  const name = agentState?.candidate_data?.name || "Candidate";
  const role = agentState?.candidate_data?.job_role || "the role";

  return (
    <div className="end-stage slide-in">
      <h1 className="end-title">
        Sorry <span>{name}</span>
      </h1>

      <p className="end-sub">
        You are not eligible for <strong>{role}</strong>
      </p>


      <button className="confirm" onClick={() => nav("/")}>
        Go Home
      </button>
    </div>
  );
}