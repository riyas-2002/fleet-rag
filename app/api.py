from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.rag.query import ask


app = FastAPI(title="Fleet RAG API")


# Request schema
class QueryRequest(BaseModel):
    query: str


# Health check
@app.get("/")
def root():
    return {"status": "Fleet RAG API is running"}


# Main endpoint
@app.post("/ask")
def query_rag(request: QueryRequest):
    response = ask(request.query)
    return {
        "query": request.query,
        "response": response
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)