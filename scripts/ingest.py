from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents

from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


def ingest():
    print("📥 Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    print("✂️ Splitting into chunks...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Connecting to Qdrant...")
    client = QdrantClient(path="qdrant_data")

    collection_name = "fleet"

    collections = client.get_collections().collections
    if collection_name not in [c.name for c in collections]:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    print("📦 Storing vectors...")

    texts = [doc.page_content for doc in chunks]
    vectors = embeddings.embed_documents(texts)

    payloads = [{"page_content": text} for text in texts]

    points = [
        PointStruct(
            id=i,
            vector=vectors[i],
            payload=payloads[i]
        )
        for i in range(len(vectors))
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest()