import streamlit as st
from config import PAGE_TITLE, PAGE_ICON
from embedding import get_embedding_model
from vector_db import get_db_client, get_collection, index_logs, query_logs
from llm import ask_llm, generate_log_summary
from ui import initialize_session_state, setup_sidebar, display_log_statistics, display_conversation, display_relevant_logs

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

initialize_session_state()

model = get_embedding_model()
client = get_db_client()

if model is None or client is None:
    st.error("Critical components failed to initialize. Please check your setup and refresh the page.")
    st.stop()

collection = get_collection(client)

st.title("📄 LLM Log Analyzer")

setup_sidebar()

uploaded_file = st.file_uploader("Upload your .log file", type=["log", "txt"])

if uploaded_file is not None:
    try:
        log_lines = [line.decode('utf-8').strip() for line in uploaded_file.readlines()]
        st.success(f"Uploaded and indexed {len(log_lines)} lines.")

        with st.spinner("Indexing logs into vector database..."):
            indexed_count = index_logs(collection, model, log_lines, st.session_state.chunk_size)
            st.write(f"Created {indexed_count} searchable log chunks.")

        display_log_statistics(log_lines)

        if st.button("Generate Log Summary"):
            with st.spinner("Generating summary..."):
                try:
                    all_chunks = [" ".join(log_lines[i:i+st.session_state.chunk_size]) for i in range(0, len(log_lines), st.session_state.chunk_size)]
                    sample_context = "\n".join(all_chunks[:min(5, len(all_chunks))])
                    summary = generate_log_summary(sample_context, [])
                    st.markdown("### 📋 Log Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Failed to generate summary: {str(e)}")

        st.session_state.logs_uploaded = True
        st.session_state.log_lines = log_lines
    except Exception as e:
        st.error(f"Failed to process the uploaded file: {str(e)}. Please ensure it's a valid text file.")

st.subheader("Ask a question about your logs")

display_conversation()

user_question = st.chat_input("e.g., 'What errors happened?' or 'Why did the service shut down?'")

if user_question:
    if collection.count() == 0:
        st.error("Please upload a log file first.")
    else:
        st.session_state.conversation.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Finding relevant logs and asking LLM..."):
            try:
                context_docs = query_logs(collection, model, user_question, st.session_state.n_results)
                context_docs = "\n".join(context_docs)

                answer = ask_llm(context_docs, user_question, st.session_state.conversation[:-1])  # Exclude current user message

                st.session_state.conversation.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
                    display_relevant_logs(context_docs)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")