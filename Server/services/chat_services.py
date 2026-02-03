from controllers.agent_controller import AgentController
from session_state import get_session, save_session
from graphs.state import AgentState
from tools.memory import get_messages, save_message
import traceback

controller = AgentController()

def process_message(session_id: str, message: str, force_step: str | None = None):
    print("\n================ PROCESS MESSAGE =================")
    print("Session:", session_id)
    print("Message:", message)
    print("Force step:", force_step)

    state = get_session(session_id)

    if not state:
        state = AgentState(session_id=session_id)


    if force_step:
        state.current_step = force_step

    state.messages.append({
        "role": "user",
        "content": message
    })

    if state.current_step != "research":
        save_message(session_id, "user", state.current_step, message)

    try:
        state = controller.step(state)

        while state.current_step == "onboarding":
            state = controller.step(state)

    except Exception as e:
        traceback.print_exc()
        return {
            "reply": "Internal error during processing.",
            "current_step": "error",
            "messages": state.messages,
            "candidate_data": state.candidate_data,
            "session_id": state.session_id
        }

    save_session(session_id, state)

    history = get_messages(session_id)

    reply = None
    if history and history[-1]["role"] == "assistant":
        reply = history[-1]["content"]
    elif state.messages:
        last = state.messages[-1]
        reply = last["content"] if isinstance(last, dict) else last


    return {
        "reply": reply,
        "current_step": state.current_step,
        "meeting_status": state.meeting_status,
        "onboarding_status": state.onboarding_status,
        "messages": state.messages,
        "candidate_data": state.candidate_data,
        "session_id": state.session_id
    }


def init_session(session_id: str, profile: dict):
    state = AgentState(
        session_id=session_id,
        candidate_data=profile,
        current_step="research"
    )
    save_session(session_id, state)
    return {"status": "session initialized"}