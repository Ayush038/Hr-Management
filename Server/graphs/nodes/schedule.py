from graphs.state import AgentState
from llm.client import client
from openai.types.responses import ResponseOutputMessage
from datetime import datetime
import re
from tools.booking import get_bookings_by_date


def scheduler_node(state: AgentState):

    if not state.messages:
        return state

    user_msg = state.messages[-1]

    today = datetime.now().strftime("%Y-%m-%d")

    extract_prompt = f"""
Today is {today}.

Extract the FULL interview slot from this message.
You MUST include:
- Calendar date (YYYY-MM-DD)
- Day name
- Time

If the user says a weekday (e.g. Monday),
infer the NEXT occurrence from today.

Return ONLY in this format:
YYYY-MM-DD Day Time

Message: "{user_msg}"

Valid examples:
- 2026-02-03 Monday 2 PM
- 2026-02-05 Wednesday 11 AM
"""

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=extract_prompt
    )

    slot = ""
    for item in resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    slot += block.text

    slot = slot.strip()

    if not slot:
        state.messages.append("I couldn't detect a time. Please repeat.")
        return state

    if not re.match(r"\d{4}-\d{2}-\d{2}", slot):
        state.messages.append("I couldn't resolve the date. Please clarify.")
        return state

    parts = slot.split()
    date_str = parts[0]

    match = re.search(r"(\d+)\s*(AM|PM)", slot, re.I)
    if not match:
        state.messages.append("I couldn't detect a valid time. Please try again.")
        return state

    hour = int(match.group(1))
    ampm = match.group(2).upper()

    if ampm == "PM" and hour != 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0


    if hour < 9 or hour > 17:
        msg = "That time is outside working hours. Please select between 9 AM and 5 PM."
        state.messages.append(msg)
        return state

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    if date_obj.date() < datetime.now().date():
        state.messages.append("That date is not available. Please choose a future date.")
        return state

    existing = get_bookings_by_date(date_str)

    if any(b["time"] == f"{hour:02d}:00" for b in existing):
        state.messages.append("That slot is already booked. Please choose another time.")
        return state

    tool_prompt = f"""
You need to book a meeting slot on a legacy calendar UI.
Which tool should you use?

Task: Click the slot "{slot}"

Available tools:
- computer_use_preview
- none

Return only the tool name.
"""

    tool_resp = client.responses.create(
        model="gpt-4o-mini",
        input=tool_prompt
    )

    tool_choice = ""
    for item in tool_resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    tool_choice += block.text

    tool_choice = tool_choice.strip()

    instruction = f"Open the calendar and click {slot}"

    state.meeting_status = {
        "slot": slot,
        "tool": tool_choice,
        "instruction": instruction,
        "status": "pending"
    }

    state.messages.append(
        f"Meeting slot '{slot}' selected. Scheduling in progress..."
    )

    state.current_step = "scheduling"
    return state