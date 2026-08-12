from agents import Agent, function_tool

from config.llm_config import model
from tools.read_document import read_document


@function_tool
def read_company_document(filename: str) -> str:
    """
    Read a specific company document.
    """

    result = read_document(filename)

    if not result["success"]:
        return result["message"]

    return (
        f"Filename: {result['filename']}\n"
        f"Category: {result['category']}\n\n"
        f"Content:\n{result['content']}"
    )


document_reader_agent = Agent(
    name="Document Reader Agent",

    instructions="""
You are the Document Reader Agent for NovaTech Solutions.

Your responsibility is to read and explain specific company
documents.

When the user asks to read or retrieve a specific document:

1. Use the read_company_document tool.
2. Return the information from the actual document.
3. Do not invent or modify company information.
4. Clearly mention the document name.
5. If the requested document does not exist, clearly say that
   the document was not found.
""",

    model=model,

    tools=[read_company_document],
)
