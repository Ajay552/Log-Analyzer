import streamlit as st
import re
from config import DEFAULT_CHUNK_SIZE, DEFAULT_N_RESULTS, ERROR_PATTERNS, setup_logging

logger = setup_logging()

def initialize_session_state():
    logger.debug("Initializing session state")
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'chunk_size' not in st.session_state:
        st.session_state.chunk_size = DEFAULT_CHUNK_SIZE
    if 'n_results' not in st.session_state:
        st.session_state.n_results = DEFAULT_N_RESULTS
    if 'logs_uploaded' not in st.session_state:
        st.session_state.logs_uploaded = False
    if 'log_lines' not in st.session_state:
        st.session_state.log_lines = []

def setup_sidebar():
    with st.sidebar:
        st.header("Settings")
        st.session_state.chunk_size = st.slider(
            "Chunk Size (lines per chunk)",
            min_value=1,
            max_value=10,
            value=st.session_state.chunk_size
        )
        st.session_state.n_results = st.slider(
            "Number of Results",
            min_value=1,
            max_value=10,
            value=st.session_state.n_results
        )

def display_log_statistics(log_lines):
    total_lines = len(log_lines)
    error_count = sum(1 for line in log_lines if re.search(ERROR_PATTERNS, line, re.IGNORECASE))
    logger.info(f"Log statistics: {total_lines} total lines, {error_count} potential issues detected")

    st.subheader("Log Statistics")
    st.write(f"Total lines: {total_lines}")
    st.write(f"Potential issues (ERROR/WARN/CRITICAL): {error_count}")

def display_conversation():
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

def display_relevant_logs(context_docs):
    with st.expander("📚 Relevant Log Snippets Used"):
        st.code(context_docs)