import re
import requests
import os
from graphs.graph import build_graph
from graphs.nodes.schedule import scheduler_node
from graphs.nodes.onboarding import onboarding_node
from graphs.state import AgentState
from tools.executor import execute_step

SERVER_URL = os.getenv("SERVER", "http://localhost:8000")

class AgentController:
    def __init__(self):
        self.graph = build_graph()

    def _to_state(self, data):
        if isinstance(data, AgentState):
            return data
        return AgentState(**data)

    def step(self, state: AgentState) -> AgentState:
        if state.current_step in ["research", "interview"]:
            result = self._to_state(self.graph.invoke(state))

            if state.current_step == "research":
                result.current_step = "interview"

            return result

        if state.current_step == "scheduling":
            state = scheduler_node(state)

            if state.meeting_status and state.meeting_status["tool"] == "computer_use_preview":
                slot = state.meeting_status["slot"]

                parts = slot.split()
                date = parts[0]

                match = re.search(r"(\d+)\s*(AM|PM)", slot, re.I)
                hour = int(match.group(1))
                if match.group(2).upper() == "PM" and hour != 12:
                    hour += 12

                res = requests.post(
                    f"{SERVER_URL}/computer/click",
                    json={"date": date, "hour": hour},
                    timeout=120
                )

                if res.status_code != 200:
                    state.messages.append("UI automation failed.")
                    return state

                data = res.json()
                if data.get("status") != "success":
                    state.messages.append("Failed to book slot via UI.")
                    return state


            return state

        if state.current_step == "onboarding":
            if not state.onboarding_status:
                state = onboarding_node(state)

            results = []
            for step in state.onboarding_status.get("steps", []):
                results.append(execute_step(step))

            state.onboarding_status["results"] = results
            state.onboarding_status["status"] = "completed"
            state.current_step = "end"
            state.messages.append("IT onboarding executed successfully.")
            return state

        return state