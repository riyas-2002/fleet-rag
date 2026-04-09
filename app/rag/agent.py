from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def rewrite_query(query: str):
    prompt = f"""
Rewrite this query to be more clear and searchable.

Query: {query}

Better query:
"""
    return llm.invoke(prompt).strip()

def evaluate_answer(context, query):
    prompt = f"""
Check if this context answers the question.

Context:
{context}

Question:
{query}

Answer YES or NO only.
"""
    return llm.invoke(prompt).strip()