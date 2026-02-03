import { useNavigate } from "react-router-dom";

export default function EndStage() {
  const nav = useNavigate();

  return (
    <div className="card big center-card slide-in">
      <h2>🎉 Welcome!</h2>
      <p>Your onboarding is complete.</p>

      <button
        className="confirm"
        onClick={() => nav("/")}
      >
        Go Home
      </button>
    </div>
  );
}
