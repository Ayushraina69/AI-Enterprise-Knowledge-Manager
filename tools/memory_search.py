from pathlib import Path
import json

from agents import function_tool


BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "memory" / "conversation_memory.json"


@function_tool
def search_memory(query: str) -> str:
    """
    Search previously saved conversation memories.
    """

    if not MEMORY_FILE.exists():
        return "No previous memories are available."

    try:
        memories = json.loads(
            MEMORY_FILE.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        return "Memory file could not be read."

    if not memories:
        return "No previous memories are available."

    query_words = query.lower().split()
    matches = []

    for memory in memories:
        text = (
            memory.get("user_question", "") + " "
            + memory.get("answer", "") + " "
            + memory.get("source", "")
        ).lower()

        score = sum(
            1 for word in query_words
            if word in text
        )

        if score > 0:
            matches.append((score, memory))

    matches.sort(
        key=lambda item: item[0],
        reverse=True
    )

    if not matches:
        return "No relevant previous memory was found."

    output = []

    for _, memory in matches[:5]:
        output.append(
            f"Previous Question: {memory['user_question']}\n"
            f"Previous Answer: {memory['answer']}\n"
            f"Source: {memory.get('source', '')}"
        )

    return "\n\n---\n\n".join(output)