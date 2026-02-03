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
        print("\n====== AGENT STEP ======")
        print("Current step:", state.current_step)

        if state.current_step in ["research", "interview"]:
            print("→ Running LangGraph node")
            result = self._to_state(self.graph.invoke(state))

            if state.current_step == "research":
                result.current_step = "interview"
                print("→ Transition: research → interview")

            return result

        if state.current_step == "scheduling":
            print("→ Entered scheduling")
            state = scheduler_node(state)

            print("Meeting status:", state.meeting_status)

            if not state.meeting_status:
                print("⚠️ No meeting_status set")
                return state

            if (
                state.meeting_status.get("tool") == "computer_use_preview"
                and state.meeting_status.get("status") != "done"
            ):
                slot = state.meeting_status["slot"]
                print("→ Running Selenium for:", slot)

                parts = slot.split()
                date = parts[0]

                match = re.search(r"(\d+)\s*(AM|PM)", slot, re.I)
                if not match:
                    state.messages.append("Invalid time format.")
                    print("❌ Time regex failed")
                    return state

                hour = int(match.group(1))
                if match.group(2).upper() == "PM" and hour != 12:
                    hour += 12

                print("→ POST /computer/click", date, hour)

                res = requests.post(
                    f"{SERVER_URL}/computer/click",
                    json={"date": date, "hour": hour},
                    timeout=120
                )

                if res.status_code != 200:
                    state.messages.append("UI automation failed.")
                    print("❌ Selenium HTTP failed")
                    return state

                data = res.json()
                print("Selenium response:", data)

                if data.get("status") != "success":
                    state.messages.append("Failed to book slot via UI.")
                    print("❌ Selenium returned error")
                    return state

                state.meeting_status["status"] = "done"
                state.current_step = "onboarding"
                print("→ Selenium done → onboarding")

            return state

        if state.current_step == "onboarding":
            print("→ Entered onboarding")

            if not state.onboarding_status:
                print("→ Generating onboarding plan")
                state = onboarding_node(state)

            results = []
            for step in state.onboarding_status.get("steps", []):
                print("→ Executing:", step)
                results.append(execute_step(step))

            state.onboarding_status["results"] = results
            state.onboarding_status["status"] = "completed"
            state.current_step = "end"
            state.messages.append("IT onboarding executed successfully.")
            print("→ Onboarding complete")

            return state

        print("⚠️ Unknown state:", state.current_step)
        return state