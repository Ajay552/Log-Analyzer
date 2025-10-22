import ollama
import sys


def analyze_logs(log_file_path, user_question):

    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()

        system_prompt = """
        You are an expert log analysis assistant.
        You will be given a log file snippet and a question.
        Analyze the log snippet to answer the question accurately.
        Focus on identifying errors, patterns, and key events.
        """

        full_prompt = f"""
        Here is the log file content:
        ---
        {log_content}
        ---

        My question is: {user_question}
        """

        print("Sending data to local LLM... (This may take a moment)")

        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': full_prompt}
            ]
        )

        print("\n--- Analysis Result ---")
        print(response['message']['content'])

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze.py <log_file_path> <user_question>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    user_question = sys.argv[2]

    analyze_logs(log_file_path, user_question)