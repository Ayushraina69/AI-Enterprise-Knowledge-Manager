from agents import Agent, function_tool

from config.llm_config import model
from tools.document_search import search_documents


@function_tool
def search_project_sop(query: str) -> str:
    """
    Search project guidelines and SOP documents.
    """

    results = search_documents(query, top_k=8)

    relevant_results = [
        result
        for result in results
        if result["category"] in ["projects", "sop"]
    ]

    if not relevant_results:
        return "No relevant project or SOP information was found."

    output = []

    for result in relevant_results[:3]:
        output.append(
            f"Source: {result['source']}\n"
            f"Category: {result['category']}\n"
            f"Content:\n{result['content']}"
        )

    return "\n\n---\n\n".join(output)


project_sop_agent = Agent(
    name="Project and SOP Agent",

    instructions="""
You are the Project and SOP Agent for NovaTech Solutions.

Your responsibility is to answer questions related to:
- Project guidelines
- Standard Operating Procedures (SOPs)
- Employee onboarding procedures

When the user asks a project or SOP-related question:

1. Use the search_project_sop tool.
2. Search only project and SOP documents.
3. Provide information based only on retrieved documents.
4. Explain procedures or guidelines clearly and step-by-step when appropriate.
5. Mention the source document.
6. Never invent company procedures or guidelines.
7. If the information is not found, clearly say that it was not found
   in the available project/SOP documents.
""",

    model=model,

    tools=[search_project_sop],
)