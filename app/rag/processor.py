from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def rewrite_query(query: str):
    prompt = f"""
Rewrite this query to be clear and searchable.

Query: {query}

Rewritten:
"""
    return llm.invoke(prompt).strip()


def classify_intent(query: str):
    prompt = f"""
Classify:

DRIVER → routes, drivers
MECHANIC → vehicle issues

Query: {query}

Answer ONLY: DRIVER or MECHANIC
"""
    res = llm.invoke(prompt).strip().upper()

    if "DRIVER" in res:
        return "DRIVER"
    return "MECHANIC"