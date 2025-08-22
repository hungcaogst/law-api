# app.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel
from openai import OpenAI
from pinecone import Pinecone

# Load env
load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT")                 # Azure OpenAI endpoint
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
LLM_API_KEY = os.getenv("LLM_API_KEY")
OPENAI_API_KEY = os.getenv("EMBEDDING_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Init clients
pc = Pinecone(api_key=PINECONE_API_KEY)

embedding_client = OpenAI()

index_name = "nd100-index"
index = pc.Index(index_name)

app = FastAPI(title="ND100 Query API")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/search")
def search_law(req: QueryRequest):
    # 1. Tạo embedding cho câu hỏi
    embedding = embedding_client.embeddings.create(
        model=EMBEDDING_MODEL_NAME,
        input=req.query
    ).data[0].embedding

    # 2. Query Pinecone
    results = index.query(
        vector=embedding,
        top_k=req.top_k,
        include_metadata=True
    )

    # 3. Chuẩn bị dữ liệu trả về
    response = [
        {
            "score": match.score,
            "text": match.metadata.get("text", "")
        }
        for match in results.matches
    ]
    return {"query": req.query, "results": response}
