from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from langchain_community.llms import Ollama

from app.rag.agent import rewrite_query,evaluate_answer
from app.rag.structured import get_routes_by_driver, get_all_drivers
from app.rag.processor import rewrite_query, classify_intent


# 🔹 GLOBAL OBJECTS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = QdrantClient(path="qdrant_data")
collection_name = "fleet"

llm = Ollama(model="llama3")


# 🔹 INTENT DETECTION (FAST + RELIABLE)

def extract_driver_name(query, drivers):
    query_lower = query.lower()

    for driver in drivers:
        if driver in query_lower:
            return driver

    return None

def ask(query: str):

    print("USER QUERY:", query)

    # STEP 1: classify
    intent = classify_intent(query)

    # STEP 2: structured route
    if intent == "DRIVER":
        drivers = get_all_drivers()
        driver = extract_driver_name(query, drivers)

        if driver:
            routes = get_routes_by_driver(driver)
            return {
                "type": "driver_result",
                "driver": driver,
                "routes": routes
            }

    # STEP 3: rewrite query
    better_query = rewrite_query(query)
    print("REWRITTEN:", better_query)

    # STEP 4: search
    query_vector = embeddings.embed_query(better_query)

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3
    )

    context = "\n".join(
        [r.payload.get("page_content", "") for r in results]
    )

    # STEP 5: evaluate
    decision = evaluate_answer(context, query)

    if "NO" in decision:
        return "Not found in data"

    # STEP 6: final answer
    prompt = f"""
Answer ONLY from context.

Context:
{context}

Question:
{query}

Answer:
"""

    return llm.invoke(prompt)