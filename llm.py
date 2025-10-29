import ollama
from config import SYSTEM_PROMPT, LLM_MODEL_NAME, setup_logging

logger = setup_logging()

def ask_llm(context, question, history):
    logger.info(f"Asking LLM with question: '{question}' (context length: {len(context)} chars, history: {len(history)} messages)")
    prompt = f"Log Snippets:\n---\n{context}\n---\nConversation History:\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nUser: {question}"

    try:
        response = ollama.chat(
            model=LLM_MODEL_NAME,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ]
        )
        logger.info("LLM response received successfully")
        return response['message']['content']
    except Exception as e:
        logger.error(f"Failed to get LLM response: {str(e)}")
        raise

def generate_log_summary(context, history):
    logger.info("Generating log summary")
    return ask_llm(context, "Provide a brief summary of the key events and issues in these log snippets.", history)