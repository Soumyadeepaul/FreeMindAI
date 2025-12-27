import streamlit as st
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

# -------------------------
# Initialize Pinecone (once)
# -------------------------
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pc.Index("my-index")

# -------------------------
# Initialize embedding model (once)
# -------------------------
embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

def vectorMatch(query: str) -> str:
    """
    Takes a query string and returns concatenated top-3
    matched context text from Pinecone.
    """

    # 1️⃣ Embed query
    q_vec = embedder.embed_query(query)

    # 2️⃣ Query Pinecone
    response = index.query(
        vector=q_vec,
        top_k=3,
        include_metadata=True
    )

    # 3️⃣ Collect matched text
    result = ""
    for match in response.get("matches", []):
        if "metadata" in match and "text" in match["metadata"]:
            result += match["metadata"]["text"] + " "

    return result.strip()
