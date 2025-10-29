import streamlit as st
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

@st.cache_resource
def get_embedding_model():
    try:
        print("Loading embedding model....")
        return SentenceTransformer(EMBEDDING_MODEL_NAME)
    except Exception as e:
        st.error(f"Failed to load embedding model: {str(e)}. Please check your internet connection and dependencies.")
        return None