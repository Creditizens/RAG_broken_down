# rag_broken_down_simply
Learn how RAG actually works by building every component separately before connecting the full system.

We start with document loading and chunking, then build embeddings and retrieval, add a local AI agent, and finally connect everything into a complete RAG pipeline using Python, LangChain and Ollama.

No magic black box—each component is coded, tested and understood on its own.

Load → Chunk → Embed → Retrieve → Agent → Answer

The complete code for this series is available free inside [Chikara Studio] (https://www.skool.com/chikara-studio-9303)

## Prerequisites

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running

Download the embedding model and create the local chat model expected by the
application:

```bash
ollama pull qwen3-embedding:4b
ollama create ministral-3-3b-8192 -f ministral-3-3b_Modelfile
```

Create a `.env` file in the project root:

```dotenv
DOCUMENT_PATH=docs/mangakissa_rules.md
SEPARATOR=<<<MANGAKISSA_RULE>>>
TOP_K=2
MOOD=friendly
```

The `.env` file is ignored by Git, so these values can be changed locally.

## Run with pip

From the project root, create and activate a virtual environment, install the
direct runtime dependencies, and start the application:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1` instead.

## Run with uv

The `pyproject.toml` contains the same direct runtime dependencies as
`requirements.txt`. From the project root, let uv create the environment,
install the dependencies, and run the application:

```bash
uv sync
uv run python app.py
```

Once the application starts, enter a question when prompted. For example:

```text
What are the rules of the mangakissa?
```

