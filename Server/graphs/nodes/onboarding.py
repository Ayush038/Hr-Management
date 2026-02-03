from graphs.state import AgentState
from llm.client import client
from openai.types.responses import ResponseOutputMessage
import re

def onboarding_node(state: AgentState):
    profile = state.candidate_data

    name = profile.get("name", "employee")
    role = profile.get("job_role", "team member")

    username = re.sub(r"[^a-z0-9_]", "_", name.lower())

    plan_prompt = f"""
You are an IT onboarding agent.

Employee name: {name}
Role: {role}

Your job is to prepare a system onboarding plan.

You must:
1. Create a folder for the user under /employees
2. Create a welcome file in that folder
3. Write a personalized welcome message
4. Verify the folder contents

Return ONLY valid JSON in this format:

{{
  "folder": "/employees/{username}",
  "steps": [
    {{ "tool": "shell", "command": "mkdir /employees/{username}" }},
    {{ "tool": "apply_patch", "file": "/employees/{username}/welcome.txt", "content": "Welcome ..." }},
    {{ "tool": "shell", "command": "ls -la /employees/{username}" }}
  ]
}}
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=plan_prompt
    )

    raw = ""
    for item in resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    raw += block.text

    match = re.search(r"\{.*\}", raw, re.S)

    if not match:
        state.messages.append("Failed to generate onboarding plan.")
        return state

    plan = eval(match.group())

    state.onboarding_status = plan
    state.onboarding_status["status"] = "pending"

    state.messages.append("IT onboarding plan generated.")
    state.current_step = "onboarding"

    return state