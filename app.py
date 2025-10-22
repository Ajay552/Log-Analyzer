import streamlit as st
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Log Analyzer 2.0")

@st.cache_resource
def get_embedding_model():
    print("Loading embedding model....")
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def get_db_client():
    print("Initializing chromaDB")
    return chromadb.Client()

model = get_embedding_model()
client = get_db_client()
collection = client.get_or_create_collection(name="logs")

def index_logs(log_lines):
    existing_ids = collection.get()['ids']
    if existing_ids:
        collection.delete(ids=existing_ids)

    chunks = [" ".join(log_lines[i:i+3]) for i in range(0, len(log_lines), 3)]
    embeddings = model.encode(chunks).tolist()
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids
    )

    return len(chunks)

def ask_llm(context, question):
    system_prompt = "You are a log expert. Answer the user's question based *only* on the provided log snippets."
    prompt = f"Log Snippets:\n---\n{context}\n---\nQuestion: {question}"

    response = ollama.chat(
        model='phi3:mini',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response['message']['content']

st.title("📄 LLM Log Analyzer")

uploaded_file = st.file_uploader("Upload your .log file", type=["log", "txt"])

if uploaded_file is not None:
    log_lines = [line.decode('utf-8').strip() for line in uploaded_file.readlines()]
    st.success(f"Uploaded and indexed {len(log_lines)} lines.")

    with st.spinner("Indexing logs into vector database..."):
        indexed_count = index_logs(log_lines)
        st.write(f"Created {indexed_count} searchable log chunks.")

st.subheader("Ask a question about your logs")
user_question = st.text_input("e.g., 'What errors happened?' or 'Why did the service shut down?'")

if st.button("Analyze"):
    if not user_question:
        st.error("Please enter a question.")
    elif collection.count() == 0:
        st.error("Please upload a log file first.")
    else:
        with st.spinner("Finding relevant logs and asking LLM..."):
            # 1. Embed the question
            question_embedding = model.encode([user_question]).tolist()

            # 2. Search ChromaDB for relevant log chunks
            results = collection.query(
                query_embeddings=question_embedding,
                n_results=5  # Get top 5 most relevant chunks
            )

            context_docs = "\n".join(results['documents'][0])

            # 3. Send to LLM
            answer = ask_llm(context_docs, user_question)

            st.markdown("### 🤖 Analysis")
            st.write(answer)

            st.markdown("### 📚 Relevant Log Snippets Used")
            st.code(context_docs)