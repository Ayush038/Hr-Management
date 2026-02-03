from graphs.state import AgentState
from llm.client import client
from openai.types.responses import ResponseOutputMessage
from datetime import datetime
import re
from tools.booking import get_bookings_by_date


def scheduler_node(state: AgentState):
    print("\n========== SCHEDULER NODE ==========")

    if not state.messages:
        print("⚠️ No messages in state")
        return state

    user_msg = state.messages[-1]
    print("👤 USER MESSAGE:", user_msg)

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

    print("🧠 Sending slot extraction prompt...")
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
    print("🧾 RAW SLOT FROM LLM:", repr(slot))

    if not slot:
        state.messages.append("I couldn't detect a time. Please repeat.")
        print("❌ Empty slot")
        return state

    if not re.match(r"\d{4}-\d{2}-\d{2}", slot):
        state.messages.append("I couldn't resolve the date. Please clarify.")
        print("❌ Invalid slot format")
        return state

    parts = slot.split()
    date_str = parts[0]
    print("📅 Parsed date:", date_str)

    match = re.search(r"(\d+)\s*(AM|PM)", slot, re.I)
    if not match:
        state.messages.append("I couldn't detect a valid time. Please try again.")
        print("❌ Time parse failed")
        return state

    hour = int(match.group(1))
    ampm = match.group(2).upper()

    if ampm == "PM" and hour != 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0

    print("⏰ Parsed hour:", hour)

    if hour < 9 or hour > 17:
        msg = "That time is outside working hours. Please select between 9 AM and 5 PM."
        state.messages.append(msg)
        print("❌ Outside work hours")
        return state

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    if date_obj.date() < datetime.now().date():
        state.messages.append("That date is not available. Please choose a future date.")
        print("❌ Past date")
        return state

    existing = get_bookings_by_date(date_str)
    print("📦 Existing bookings:", existing)

    if any(b["time"] == f"{hour:02d}:00" for b in existing):
        state.messages.append("That slot is already booked. Please choose another time.")
        print("❌ Slot conflict")
        return state

    print("🧠 Asking tool selector LLM...")
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
    print("🔧 TOOL CHOSEN:", tool_choice)

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
    print("✅ Scheduler complete → state = scheduling")
    print("====================================\n")
    return state