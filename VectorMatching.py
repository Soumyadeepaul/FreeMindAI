from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


def vectorMatch(query):
    
    # -------------------------
    # 1. Initialize Pinecone
    # -------------------------
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("my-index")

    # -------------------------
    # 2. Embedding model
    # -------------------------
    embedder = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # -------------------------
    # 3. Ask your query
    # -------------------------
    # query = "What is human behaviour?"   # <-- your question

    q_vec = embedder.embed_query(query)

    # -------------------------
    # 4. Query Pinecone (top 3)
    # -------------------------
    response = index.query(
        vector=q_vec,
        top_k=3,
        include_metadata=True
    )

    # -------------------------
    # 5. Print results
    # -------------------------
    result=""
    for i, match in enumerate(response["matches"]):
        result+=match["metadata"]["text"]+" "
    return result
