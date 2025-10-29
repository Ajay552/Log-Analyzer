import ollama
from config import SYSTEM_PROMPT, LLM_MODEL_NAME

def ask_llm(context, question, history):
    prompt = f"Log Snippets:\n---\n{context}\n---\nConversation History:\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nUser: {question}"

    response = ollama.chat(
        model=LLM_MODEL_NAME,
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response['message']['content']

def generate_log_summary(context, history):
    return ask_llm(context, "Provide a brief summary of the key events and issues in these log snippets.", history)