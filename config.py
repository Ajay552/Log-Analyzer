import streamlit as st

PAGE_TITLE = "Log Analyzer 2.0"
PAGE_ICON = "📄"

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
LLM_MODEL_NAME = 'phi3:mini'

DEFAULT_CHUNK_SIZE = 3
DEFAULT_N_RESULTS = 5

COLLECTION_NAME = "logs"

ERROR_PATTERNS = r'\bERROR\b|\bWARN\b|\bCRITICAL\b'

SYSTEM_PROMPT = "You are a log expert. Answer the user's question based *only* on the provided log snippets. Maintain conversation context."