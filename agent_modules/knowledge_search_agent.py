from agents import Agent, function_tool

from config.llm_config import model
from tools.document_search import search_documents


@function_tool
def knowledge_search(query: str) -> str:
    """
    Search the NovaTech enterprise knowledge base
    and return the most relevant information.
    """

    results = search_documents(query, top_k=3)

    if not results:
        return "No relevant information was found."

    output = []

    for result in results:
        output.append(
            f"Source: {result['source']}\n"
            f"Category: {result['category']}\n"
            f"Content: {result['content']}"
        )

    return "\n\n---\n\n".join(output)


knowledge_search_agent = Agent(
    name="Knowledge Search Agent",

    instructions="""
You are the Knowledge Search Agent for NovaTech Solutions.

Your responsibility is to find relevant information from the
company's internal knowledge base.

When the user asks a question:

1. Use the knowledge_search tool.
2. Base your answer only on the retrieved company information.
3. Mention the source document when providing factual information.
4. If the information cannot be found, clearly say that it
   was not found in the available company knowledge.
5. Do not invent company policies, decisions, or facts.
""",

    model=model,

    tools=[knowledge_search],
)