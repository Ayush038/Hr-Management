from controllers.agent_controller import AgentController
from session_state import get_session, save_session
from graphs.state import AgentState
from tools.memory import get_messages, save_message

controller = AgentController()

def process_message(session_id: str, message: str):
    state = get_session(session_id)

    if not state:
        state = AgentState(session_id=session_id)

    state.messages.append(message)

    if state.current_step != "research":
        save_message(session_id, "user", state.current_step, message)

    state = controller.step(state)
    while state.current_step == "onboarding":
        state = controller.step(state)
    save_session(session_id, state)

    history = get_messages(session_id)

    reply = None
    if history and history[-1]["role"] == "assistant":
        reply = history[-1]["content"]
    elif state.messages:
        reply = state.messages[-1]

    return {
        "reply": reply,
        "current_step": state.current_step,
        "meeting_status": state.meeting_status,
        "onboarding_status": state.onboarding_status,
    }




def init_session(session_id: str, profile: dict):
    state = AgentState(
        session_id=session_id,
        candidate_data=profile,
        current_step="research"
    )
    save_session(session_id, state)
    return {"status": "session initialized"}