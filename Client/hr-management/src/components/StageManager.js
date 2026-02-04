import { useEffect } from "react";
import Swal from "sweetalert2";
import ResearchStage from "../stageManager/ResearchStage";
import InterviewStage from "../stageManager/InterviewStage";
import ScheduleStage from "../stageManager/ScheduleStage";
import EndStage from "../stageManager/EndStage";
import RejectedStage from "../stageManager/RejectedStage";

export default function StageManager({ sessionId, agentState, setAgentState }) {
  const step = agentState?.current_step || "research";

  useEffect(() => {
    if (step === "scheduling") {
      Swal.fire({
        title: "Interview Passed",
        text: "Let’s schedule your slot",
        icon: "success",
        background: "linear-gradient(135deg, rgba(30,41,59,.9), rgba(2,6,23,.95))",
        color: "#e5e7eb",
        confirmButtonColor: "#38bdf8"
      });
    }
    if (step === "rejected") {
      Swal.fire({
        title: "Not Selected",
        text: "Unfortunately, you did not clear the interview.",
        icon: "error",
        background: "linear-gradient(135deg, rgba(30,41,59,.9), rgba(2,6,23,.95))",
        color: "#e5e7eb",
        confirmButtonColor: "#ef4444"
      });
    }
    if (step === "end") {
      Swal.fire({
        title: "Process Completed",
        icon: "info",
        background: "linear-gradient(135deg, rgba(30,41,59,.9), rgba(2,6,23,.95))",
        color: "#e5e7eb",
        confirmButtonColor: "#38bdf8"
      });
    }
  }, [step]);

  return (
    <div className="stage">
      {step === "research" && (
        <ResearchStage sessionId={sessionId} setAgentState={setAgentState} />
      )}

      {step === "interview" && (
        <InterviewStage
          sessionId={sessionId}
          agentState={agentState}
          setAgentState={setAgentState}
        />
      )}

      {step === "scheduling" && (
        <ScheduleStage agentState={agentState} setAgentState={setAgentState} />
      )}

      {step === "end" && <EndStage agentState={agentState} />}
      {step === "rejected" && <RejectedStage agentState={agentState} />}
    </div>
  );
}