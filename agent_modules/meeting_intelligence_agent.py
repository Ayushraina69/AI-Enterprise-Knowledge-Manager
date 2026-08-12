from agents import Agent, function_tool

from config.llm_config import model
from tools.document_search import search_documents


@function_tool
def search_meeting_notes(query: str) -> str:
    """
    Search specifically within company meeting notes.
    """

    results = search_documents(query, top_k=8)

    meeting_results = [
        result
        for result in results
        if result["category"] == "meetings"
    ]

    if not meeting_results:
        return "No relevant meeting information was found."

    output = []

    for result in meeting_results[:3]:
        output.append(
            f"Source: {result['source']}\n"
            f"Content:\n{result['content']}"
        )

    return "\n\n---\n\n".join(output)


meeting_intelligence_agent = Agent(
    name="Meeting Intelligence Agent",

    instructions="""
You are the Meeting Intelligence Agent for NovaTech Solutions.

Your responsibility is to analyze company meeting notes.

When the user asks about meetings:

1. Use the search_meeting_notes tool.
2. Search only meeting-related information.
3. Identify important discussions, decisions, action items,
   responsibilities, and follow-ups when available.
4. Give a clear and structured answer.
5. Mention the source meeting document.
6. Do not invent information that is not present in the meeting notes.
7. If the requested information cannot be found, clearly say so.
""",

    model=model,

    tools=[search_meeting_notes],
)
