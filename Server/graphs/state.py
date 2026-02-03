from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class AgentState:
    session_id: str = ""
    messages: List[str] = field(default_factory=list)
    current_step: str = "research"
    candidate_data: Dict[str, Any] = field(default_factory=dict)
    meeting_status: Dict[str, Any] = field(default_factory=dict)
    onboarding_status: Dict[str, Any] = field(default_factory=dict)