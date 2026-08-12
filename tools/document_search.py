from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = BASE_DIR / "vector_db"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_DIR)
)

collection = client.get_collection(
    name="novatech_knowledge"
)


def search_documents(query: str, top_k: int = 3):

    query_lower = query.lower()

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=8
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    results_list = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        source = metadata.get("source", "").lower()

        score = 0

        # Work-from-home queries
        if any(word in query_lower for word in [
            "work from home",
            "wfh",
            "remote",
            "remote work"
        ]):
            if "wfh" in source:
                score += 10

        # Leave queries
        if any(word in query_lower for word in [
            "leave",
            "casual leave",
            "sick leave"
        ]):
            if "leave" in source:
                score += 10

        # Security queries
        if any(word in query_lower for word in [
            "security",
            "password",
            "mfa",
            "multi-factor",
            "suspicious email"
        ]):
            if "security" in source:
                score += 10

        # Expense queries
        if any(word in query_lower for word in [
            "expense",
            "reimbursement",
            "receipt"
        ]):
            if "expense" in source:
                score += 10

        # Meeting queries
        if "product" in query_lower and "meeting" in query_lower:
            if "product_meeting" in source:
                score += 10

        if "sales" in query_lower and "meeting" in query_lower:
            if "sales_meeting" in source:
                score += 10

        # Onboarding queries
        if any(word in query_lower for word in [
            "onboarding",
            "new employee",
            "joining"
        ]):
            if "onboarding" in source:
                score += 10

        # Project queries
        if any(word in query_lower for word in [
            "project",
            "project scope",
            "project guidelines"
        ]):
            if "project_guidelines" in source:
                score += 10

        results_list.append(
            {
                "content": document,
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "category": metadata.get(
                    "category",
                    "Unknown"
                ),
                "distance": round(distance, 4),
                "score": score,
            }
        )

    # First use relevance score, then semantic distance
    results_list.sort(
        key=lambda x: (-x["score"], x["distance"])
    )

    return results_list[:top_k]


if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    results = search_documents(question)

    print("\nSearch Results")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {index}")
        print(f"Source: {result['source']}")
        print(f"Category: {result['category']}")
        print(f"Relevance Score: {result['score']}")
        print(f"Distance: {result['distance']}")
        print(f"Content:\n{result['content']}")