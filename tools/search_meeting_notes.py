from document_search import search_documents


def search_meeting_notes(query: str):
    """
    Search specifically within company meeting notes.
    """

    results = search_documents(
        query,
        top_k=8
    )

    meeting_results = [
        result
        for result in results
        if result["category"] == "meetings"
    ]

    return meeting_results[:3]


if __name__ == "__main__":

    question = input(
        "Enter your meeting question: "
    )

    results = search_meeting_notes(question)

    print("\nMeeting Search Results")
    print("=" * 60)

    if not results:
        print("No relevant meeting notes found.")

    else:
        for index, result in enumerate(
            results,
            start=1
        ):
            print(f"\nResult {index}")
            print(f"Source: {result['source']}")
            print(f"Content:\n{result['content']}")