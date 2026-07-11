# EBook Expert Assistant

This project is a simple Retrieval-Augmented Generation (RAG) application that lets you chat with the content of your EPUB books. It ingests EPUB files from a local knowledge base, creates embeddings, stores them in a local Chroma vector database, and then uses an Ollama language model to answer questions with relevant retrieved context.

## What this app does

- Loads EPUB files from the `knowledge-base` folder
- Splits the book content into smaller chunks
- Creates vector embeddings and stores them locally with Chroma
- Retrieves relevant chunks for each question
- Uses an LLM to answer questions based on retrieved context
- Provides a Gradio web interface for chatting

## Project structure

```text
app.py                    # Gradio web app entry point
pipelines/
  chat.py                 # Question answering logic
  ingest.py               # EPUB ingestion and embedding creation
knowledge-base/          # Place your .epub files here
bookstore_vector_db/     # Local vector database created by ingestion
```

## Prerequisites

Before installing the app, make sure you have:

- Python 3.10 or newer
- Windows PowerShell or Command Prompt
- Ollama installed and running locally
- An internet connection to download the required Python packages and the Ollama model

## Install Ollama

This app uses Ollama for the language model.

1. Install Ollama from the official website:
   https://ollama.com/
2. After installation, open a terminal and pull the default model used by the app:

```powershell
ollama pull gemma3:1b
```

3. Start the Ollama service:

```powershell
ollama serve
```

Keep this terminal open while using the app.

## Install the application

### Option 1: Recommended with uv

This project is designed to work well with `uv`, which makes dependency management simpler.

1. Open PowerShell in the project root folder.

2. Install `uv` if it is not installed yet:

```powershell
py -m pip install uv
```

3. Create a virtual environment:

```powershell
uv venv .venv
```

4. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

5. Install the required Python packages:

```powershell
uv pip install gradio langchain-ollama langchain-chroma langchain-huggingface langchain-community langchain-text-splitters unstructured
```

### Option 2: Install with pip

If you prefer not to use `uv`, you can install the packages with `pip`:

```powershell
py -m pip install gradio langchain-ollama langchain-chroma langchain-huggingface langchain-community langchain-text-splitters unstructured
```

## Prepare your books

1. Place your EPUB files inside the `knowledge-base` folder.
2. If you already have books in that folder, the ingestion step will process them automatically.
3. If you want to rebuild the vector database from scratch, delete or rename the existing `bookstore_vector_db` folder first.

## Build the vector database

The ingestion script reads all EPUB files from `knowledge-base`, splits them into chunks, creates embeddings, and stores them locally.

Run:

```powershell
uv run python pipelines/ingest.py
```

If you used `pip` instead of `uv`, use:

```powershell
python pipelines/ingest.py
```

You should see a message like:

```text
Ingestion complete
```

## Run the application

Start the Gradio interface:

```powershell
uv run python app.py
```

Or with `pip`:

```powershell
python app.py
```

A browser window should open automatically. If it does not, the terminal will print a local URL you can copy and open manually.

## How to use it

1. Open the app in your browser.
2. Type a question about the content of your books in the chat box.
3. The assistant will use the stored book context to respond.
4. The right-side panel shows the retrieved context used for the answer.
5. You can ask follow-up questions in the same conversation.

## Notes

- The default LLM model is `gemma3:1b`.
- You can change the model by editing the `MODEL` value in `pipelines/chat.py`.
- The app expects EPUB files in `knowledge-base` before ingestion is run.
- If you add new books later, re-run `pipelines/ingest.py` so the vector database is updated.

## Troubleshooting

### Ollama model not found

If you get an error that the model cannot be found, run:

```powershell
ollama pull gemma3:1b
```

### No answers or empty context

- Make sure your EPUB files are in `knowledge-base`
- Re-run the ingestion script
- Confirm the Ollama service is running

### Import errors

If Python reports missing packages, reinstall them using the command from the installation section.

## License

This project is intended for local use and experimentation.
