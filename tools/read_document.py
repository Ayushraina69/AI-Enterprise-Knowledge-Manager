from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def read_document(filename: str):
    """
    Read a company knowledge document by filename.
    """

    matching_files = list(DATA_DIR.rglob(filename))

    if not matching_files:
        return {
            "success": False,
            "message": f"Document '{filename}' was not found."
        }

    file_path = matching_files[0]

    content = file_path.read_text(
        encoding="utf-8"
    )

    return {
        "success": True,
        "filename": file_path.name,
        "category": file_path.parent.name,
        "content": content
    }


if __name__ == "__main__":

    filename = input(
        "Enter document filename: "
    )

    result = read_document(filename)

    print("\nDocument Result")
    print("=" * 60)

    if result["success"]:
        print(f"Filename: {result['filename']}")
        print(f"Category: {result['category']}")
        print("\nContent:")
        print(result["content"])
    else:
        print(result["message"])