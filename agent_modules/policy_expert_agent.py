from agents import Agent, function_tool

from config.llm_config import model
from tools.search_policy import search_policy


@function_tool
def search_company_policy(question: str) -> str:
    """
    Search the company policy knowledge base.
    """

    results = search_policy(question)

    if not results:
        return "No relevant company policy was found."

    output = []

    for result in results:
        output.append(
            f"Source: {result['source']}\n"
            f"Content: {result['content']}"
        )

    return "\n\n---\n\n".join(output)


policy_expert_agent = Agent(
    name="Policy Expert Agent",

    instructions="""
You are the Policy Expert Agent for NovaTech Solutions.

Your responsibility is to answer questions specifically about
company policies.

When the user asks a policy-related question:

1. Use the search_company_policy tool.
2. Base your answer only on retrieved company policy information.
3. Clearly mention the policy document used as the source.
4. Give a concise and easy-to-understand answer.
5. Never invent or assume company policies.
6. If the required policy information cannot be found, clearly
   say that it was not found in the available company policies.
""",

    model=model,

    tools=[search_company_policy],
)