from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_db"


# Load local embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Create persistent ChromaDB database
client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

collection = client.get_or_create_collection(
    name="novatech_knowledge"
)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """Split document text into overlapping chunks."""
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_documents():
    txt_files = list(DATA_DIR.rglob("*.txt"))

    if not txt_files:
        print("No .txt documents found.")
        return

    total_chunks = 0

    for file_path in txt_files:
        print(f"Processing: {file_path.name}")

        text = file_path.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        embeddings = embedding_model.encode(
            chunks,
            normalize_embeddings=True
        ).tolist()

        ids = [
            f"{file_path.stem}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "source": file_path.name,
                "category": file_path.parent.name,
            }
            for _ in chunks
        ]

        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)

    print("\nKnowledge base created successfully!")
    print(f"Documents processed: {len(txt_files)}")
    print(f"Total chunks stored: {total_chunks}")
    print(f"Vector database: {VECTOR_DB_DIR}")


if __name__ == "__main__":
    ingest_documents()
    