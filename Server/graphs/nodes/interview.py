from graphs.state import AgentState
from llm.client import client
from tools.memory import save_message, save_evaluation, get_messages, get_evaluations
from openai.types.responses import ResponseOutputMessage
import json
import re


def _safe_scores(raw: str):
    try:
        data = json.loads(raw.strip())
        return {
            "technical": float(data.get("technical", 0)),
            "depth": float(data.get("depth", 0)),
            "clarity": float(data.get("clarity", 0)),
        }
    except Exception:
        print("EVAL PARSE FAILED:", raw)
        return {"technical": 0, "depth": 0, "clarity": 0}


def interview_node(state: AgentState):
    session = state.session_id
    profile = state.candidate_data

    history = get_messages(session)

    if not any(m["stage"] == "interview" for m in history):
        prompt = f"""
You are an HR interviewer.

Candidate profile:
Name: {profile.get("name")}
Role: {profile.get("job_role")}
Experience: {profile.get("experience")}
Skills: {profile.get("skills")}

Ask ONE short technical screening question relevant to this role.
"""
        resp = client.responses.create(model="gpt-4o-mini", input=prompt)

        question = ""
        for item in resp.output:
            if isinstance(item, ResponseOutputMessage):
                for block in item.content:
                    if block.type == "output_text":
                        question += block.text

        question = question.strip() or "Tell me about your technical background."
        save_message(session, "assistant", "interview", question)

        state.messages.append({
            "role": "assistant",
            "content": question
        })
        return state

    if history[-1]["role"] == "assistant" and history[-1]["stage"] == "interview":
        return state

    if len(history) < 2:
        return state

    last_q = history[-2]["content"]
    last_a = history[-1]["content"]

    eval_prompt = f"""
You are an interview evaluator.

Score generously.
Assume the candidate is junior–mid level.
Do NOT be strict.

Scoring rules:
- 8–10 = strong, correct, well-explained
- 6–7 = good, mostly correct
- 4–5 = partial or vague
- 1–3 = wrong or off-topic

Return ONLY valid JSON.
No explanation. No markdown. No extra text.

Format EXACTLY like:
{{"technical": 0, "depth": 0, "clarity": 0}}

Question:
{last_q}

Answer:
{last_a}
"""
    eval_resp = client.responses.create(model="gpt-4o-mini", input=eval_prompt)

    raw = ""
    for item in eval_resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    raw += block.text

    scores = _safe_scores(raw)
    save_evaluation(session, last_q, last_a, scores)

    all_evals = get_evaluations(session)
    evaluations = all_evals[-3:]

    if len(all_evals) >= 8:
        msg = "Thank you for your time. We will review your performance."
        save_message(session, "assistant", "interview", msg)
        state.messages.append({"role": "assistant", "content": msg})
        state.current_step = "rejected"
        return state

    total = 0
    for ev in evaluations:
        s = ev.get("scores", {})
        total += (
            float(s.get("technical", 0)) * 0.5 +
            float(s.get("depth", 0)) * 0.3 +
            float(s.get("clarity", 0)) * 0.2
        )

    avg = total / len(evaluations) if evaluations else 0

    if avg < 2.5:
        msg = "Unfortunately, your answers did not meet the technical bar."
        save_message(session, "assistant", "interview", msg)
        state.messages.append({"role": "assistant", "content": msg})
        state.current_step = "rejected"
        return state

    if 2.5 <= avg < 6:
        followup_prompt = f"""
Ask another technical question at the SAME difficulty.

Question:
{last_q}

Answer:
{last_a}
"""
        f_resp = client.responses.create(model="gpt-4o-mini", input=followup_prompt)

    elif 6 <= avg < 7.5:
        followup_prompt = f"""
Ask a HARDER follow-up question that probes deeper.

Question:
{last_q}
Answer:
{last_a}
"""
        f_resp = client.responses.create(model="gpt-4o-mini", input=followup_prompt)

    else:
        strong = 0
        for ev in evaluations:
            s = ev.get("scores", {})
            score = (
                float(s.get("technical", 0)) * 0.5 +
                float(s.get("depth", 0)) * 0.3 +
                float(s.get("clarity", 0)) * 0.2
            )
            if score >= 7.5:
                strong += 1

        if strong >= 2:
            msg = "Congratulations! You have passed the interview."
            save_message(session, "assistant", "interview", msg)
            state.messages.append({"role": "assistant", "content": msg})
            state.current_step = "scheduling"
            return state
        else:
            followup_prompt = f"""
Ask one final HARD technical follow-up to confirm skill.

Question:
{last_q}
Answer:
{last_a}
"""
            f_resp = client.responses.create(model="gpt-4o-mini", input=followup_prompt)

    if "f_resp" not in locals():
        follow = "Can you go into more technical detail?"
        save_message(session, "assistant", "interview", follow)
        state.messages.append({"role": "assistant", "content": follow})
        return state

    follow = ""
    for item in f_resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    follow += block.text

    follow = follow.strip() or "Can you explain this in more detail?"
    save_message(session, "assistant", "interview", follow)
    state.messages.append({"role": "assistant", "content": follow})
    return state