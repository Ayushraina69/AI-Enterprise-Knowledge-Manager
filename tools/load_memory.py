from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_FILE = MEMORY_DIR / "conversation_memory.json"


def load_memory(limit: int = 5):
    """
    Load recent conversation memories.
    """

    if not MEMORY_FILE.exists():
        return []

    try:
        memories = json.loads(
            MEMORY_FILE.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:
        return []

    return memories[-limit:]


if __name__ == "__main__":

    memories = load_memory()

    print("\nConversation Memory")
    print("=" * 60)

    if not memories:
        print("No memories found.")
    else:
        for memory in memories:
            print(f"\nQuestion: {memory['user_question']}")
            print(f"Answer: {memory['answer']}")
            print(f"Source: {memory['source']}")
            print(f"Time: {memory['timestamp']}")
            