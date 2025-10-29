import chromadb
import streamlit as st
from config import COLLECTION_NAME, setup_logging

logger = setup_logging()

@st.cache_resource
def get_db_client():
    try:
        logger.info("Initializing chromaDB")
        return chromadb.Client()
    except Exception as e:
        logger.error(f"Failed to initialize ChromaDB: {str(e)}")
        st.error(f"Failed to initialize ChromaDB: {str(e)}.")
        return None

def get_collection(client):
    return client.get_or_create_collection(name=COLLECTION_NAME)

def index_logs(collection, model, log_lines, chunk_size):
    try:
        logger.info(f"Starting to index {len(log_lines)} log lines with chunk size {chunk_size}")
        existing_ids = collection.get()['ids']
        if existing_ids:
            logger.info(f"Clearing {len(existing_ids)} existing documents from collection")
            collection.delete(ids=existing_ids)

        chunks = [" ".join(log_lines[i:i+chunk_size]) for i in range(0, len(log_lines), chunk_size)]
        logger.info(f"Created {len(chunks)} chunks for indexing")
        embeddings = model.encode(chunks).tolist()
        ids = [str(i) for i in range(len(chunks))]

        collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids
        )
        logger.info(f"Successfully indexed {len(chunks)} log chunks")
        return len(chunks)
    except Exception as e:
        logger.error(f"Failed to index logs: {str(e)}")
        raise Exception(f"Failed to index logs: {str(e)}")

def query_logs(collection, model, question, n_results):
    logger.info(f"Querying logs with question: '{question}' for {n_results} results")
    question_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )

    found_results = len(results['documents'][0]) if results['documents'] else 0
    logger.info(f"Found {found_results} relevant log chunks")
    return results['documents'][0]