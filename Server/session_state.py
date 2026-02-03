from graphs.state import AgentState

SESSIONS = {}

def get_session(session_id: str) -> AgentState:
    return SESSIONS.get(session_id)

def save_session(session_id: str, state: AgentState):
    SESSIONS[session_id] = state