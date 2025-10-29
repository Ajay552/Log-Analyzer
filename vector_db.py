import chromadb
import streamlit as st
from config import COLLECTION_NAME

@st.cache_resource
def get_db_client():
    try:
        print("Initializing chromaDB")
        return chromadb.Client()
    except Exception as e:
        st.error(f"Failed to initialize ChromaDB: {str(e)}.")
        return None

def get_collection(client):
    return client.get_or_create_collection(name=COLLECTION_NAME)

def index_logs(collection, model, log_lines, chunk_size):
    try:
        existing_ids = collection.get()['ids']
        if existing_ids:
            collection.delete(ids=existing_ids)

        chunks = [" ".join(log_lines[i:i+chunk_size]) for i in range(0, len(log_lines), chunk_size)]
        embeddings = model.encode(chunks).tolist()
        ids = [str(i) for i in range(len(chunks))]

        collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids
        )

        return len(chunks)
    except Exception as e:
        raise Exception(f"Failed to index logs: {str(e)}")

def query_logs(collection, model, question, n_results):
    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )

    return results['documents'][0]