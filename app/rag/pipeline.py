from .retriever import retrieve
from .llm import generate_answer
from .structured import get_routes_by_driver

def run_rag(db, query):
    
    # Simple rule-based routing
    if "route" in query.lower() and "does" in query.lower():
        name = query.split("does")[-1].strip().split()[0]
        routes = get_routes_by_driver(name)

        if routes:
            return f"{name} has worked on routes: {', '.join(routes)}"
        else:
            return f"No routes found for {name}"

    # Default → RAG
    docs = retrieve(db, query)
    context = "\n".join([d.page_content for d in docs])

    return generate_answer(context, query)