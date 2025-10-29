import streamlit as st
import logging
import os
from datetime import datetime

PAGE_TITLE = "Log Analyzer 2.0"
PAGE_ICON = "📄"

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
LLM_MODEL_NAME = 'phi4-mini:3.8b'

DEFAULT_CHUNK_SIZE = 3
DEFAULT_N_RESULTS = 5

COLLECTION_NAME = "logs"

ERROR_PATTERNS = r'\bERROR\b|\bWARN\b|\bCRITICAL\b'

SYSTEM_PROMPT = "You are a log expert. Answer the user's question based *only* on the provided log snippets. Maintain conversation context."

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, f"log_analyzer_{datetime.now().strftime('%Y%m%d')}.log")

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('log_analyzer')
    return logger