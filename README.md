# Log Analyzer 2.0

A Streamlit-based application that uses embeddings and a local LLM (via Ollama) to analyze and answer questions about log files.

## Features

- Upload log files (.log or .txt)
- Automatic indexing of logs into a vector database using sentence embeddings
- Query logs with natural language questions
- Get AI-powered analysis based on relevant log snippets

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

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is installed and the required model is available:
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
3. Enter a question about your logs in the text input (e.g., "What errors occurred?" or "Why did the service restart?")
4. Click "Analyze" to get an AI-generated answer based on relevant log snippets

## Sample Logs

Check the `sample-logs/` directory for example log files to test with.

## Dependencies

- Streamlit: Web app framework
- Ollama: Local LLM interface
- ChromaDB: Vector database for embeddings
- Sentence Transformers: For generating text embeddings

## Troubleshooting

- Ensure Ollama is running before starting the app
- If you encounter embedding model loading issues, check your internet connection for the initial download
- For large log files, indexing may take some time