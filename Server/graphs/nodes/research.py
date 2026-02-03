from graphs.state import AgentState
from llm.client import client
from openai.types.responses import ResponseOutputMessage


def research_node(state: AgentState):
    if not state.messages:
        state.messages.append("No query provided.")
        return state

    query = state.messages[-1]

    resp = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=f"""
You are a HR research agent.

Use web_search_preview to find reliable information about: {query}.
Then summarize the key facts in under 120 words.
Only use the tool results.
"""
    )

    summary = []
    for item in resp.output:
        if isinstance(item, ResponseOutputMessage):
            for block in item.content:
                if block.type == "output_text":
                    summary.append(block.text)

    final_summary = "\n".join(summary).strip()

    if not final_summary:
        state.messages.append("No research summary generated.")
        return state

    state.candidate_data["research_summary"] = final_summary
    state.messages.append(final_summary)

    return state