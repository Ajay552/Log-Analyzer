# Log Analyzer 2.0

A Streamlit-based application that uses embeddings and a local LLM (via Ollama) to analyze and answer questions about log files.

## Features

- Upload log files (.log or .txt)
- Automatic indexing of logs into a vector database using sentence embeddings
- Configurable chunk size and number of search results
- Generate AI-powered log summaries
- Query logs with natural language questions via chat interface
- Get AI-powered analysis based on relevant log snippets
- View log statistics and error counts

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- The `phi3:mini` model pulled in Ollama (`ollama pull phi3:mini`)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd log-analyzer-cli
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Ollama is installed and the required model is available:
   ```bash
   ollama pull phi3:mini
   ```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

This will open a web browser with the application running locally.

## Usage

1. Upload a log file using the file uploader (supports .log and .txt files)
2. The app will index the log lines into chunks and store them in a vector database
3. Adjust settings in the sidebar (chunk size for indexing, number of results for queries)
4. View log statistics showing total lines and potential issues
5. Click "Generate Log Summary" for an AI-generated overview of key events
6. Ask questions about your logs using the chat input (e.g., "What errors occurred?" or "Why did the service restart?")
7. Get AI-generated answers based on relevant log snippets, with the option to view the source logs used

## Sample Logs

Check the `sample-logs/` directory for example log files to test with.

## Dependencies

- **Streamlit**: Web app framework
- **Ollama**: Local LLM interface
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: For generating text embeddings (uses `all-MiniLM-L6-v2` model)
- **Python 3.8+**: Runtime environment

See `requirements.txt` for the complete list of dependencies.

## Troubleshooting

- Ensure Ollama is running before starting the app
- Verify the `phi3:mini` model is pulled: `ollama pull phi3:mini`
- If you encounter embedding model loading issues, check your internet connection for the initial download
- For large log files, indexing may take some time
- Adjust chunk size in settings for better performance with very large files