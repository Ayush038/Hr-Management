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
        print("⚠️ No session found, creating new one")
        state = AgentState(session_id=session_id)

    print("➡️ Current step BEFORE:", state.current_step)

    if force_step:
        print("⚠️ Forcing step to:", force_step)
        state.current_step = force_step

    state.messages.append({
        "role": "user",
        "content": message
    })

    if state.current_step != "research":
        save_message(session_id, "user", state.current_step, message)

    try:
        print("🧠 Calling controller.step() ...")
        state = controller.step(state)
        print("➡️ Step AFTER controller:", state.current_step)

        while state.current_step == "onboarding":
            print("🔁 Auto onboarding step...")
            state = controller.step(state)
            print("➡️ Step NOW:", state.current_step)

    except Exception as e:
        print("🔥 ERROR inside controller.step():", e)
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
    print("📜 History length:", len(history))

    reply = None
    if history and history[-1]["role"] == "assistant":
        reply = history[-1]["content"]
    elif state.messages:
        last = state.messages[-1]
        reply = last["content"] if isinstance(last, dict) else last

    print("✅ Returning step:", state.current_step)
    print("==================================================\n")

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
    print("🆕 INIT SESSION:", session_id)
    state = AgentState(
        session_id=session_id,
        candidate_data=profile,
        current_step="research"
    )
    save_session(session_id, state)
    return {"status": "session initialized"}