from pathlib import Path
import json
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_FILE = MEMORY_DIR / "conversation_memory.json"


def save_memory(
    user_question: str,
    answer: str,
    source: str = ""
):
    """
    Save an important interaction to local memory.
    """

    MEMORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if MEMORY_FILE.exists():
        try:
            memories = json.loads(
                MEMORY_FILE.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError:
            memories = []
    else:
        memories = []

    memory = {
        "timestamp": datetime.now().isoformat(),
        "user_question": user_question,
        "answer": answer,
        "source": source
    }

    memories.append(memory)

    MEMORY_FILE.write_text(
        json.dumps(
            memories,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return {
        "success": True,
        "message": "Memory saved successfully.",
        "memory": memory
    }


if __name__ == "__main__":

    question = input(
        "Enter user question: "
    )

    answer = input(
        "Enter answer: "
    )

    source = input(
        "Enter source (optional): "
    )

    result = save_memory(
        question,
        answer,
        source
    )

    print("\nMemory Result")
    print("=" * 60)
    print(result["message"])