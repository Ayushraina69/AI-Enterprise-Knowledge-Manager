from pathlib import Path

from tools.document_search import search_documents


def search_policy(query: str):
    """
    Search specifically within company policy documents.
    """

    results = search_documents(
        query,
        top_k=8
    )

    policy_results = [
        result
        for result in results
        if result["category"] == "policies"
    ]

    return policy_results[:3]


if __name__ == "__main__":

    question = input(
        "Enter your policy question: "
    )

    results = search_policy(question)

    print("\nPolicy Search Results")
    print("=" * 60)

    if not results:
        print("No relevant policy found.")
    else:
        for index, result in enumerate(
            results,
            start=1
        ):
            print(f"\nResult {index}")
            print(f"Source: {result['source']}")
            print(f"Content:\n{result['content']}")