# FundFacts (SchemeSaathi)

FundFacts is a SEBI-grounded mutual-fund education assistant. SchemeSaathi uses retrieval-augmented generation (RAG) to answer beginner questions from retrieved SEBI reference chunks while strictly avoiding personalised investment advice.

## Features
- **SEBI-Grounded RAG**: Answers generated only from official SEBI investor education chunks with verified citations.
- **Lightweight ONNX Embedding**: Vector search powered by ChromaDB's built-in ONNX runtime (zero PyTorch overhead).
- **FastAPI Backend**: Complete REST API providing `/health`, `/records`, `/search`, `/ask`, `/chat`, and `/agent`.
- **Streamlit Interface**: Interactive chat UI with citation expansion, SIP rupee-cost averaging calculator, and feedback.
- **LangGraph Agent Workflow**: Interactive conversation memory with explicit human approval checkpoints.
- **Render Ready**: Optimized for Render free tier deployment (< 200 MB image footprint, < 60 MB RAM).

## Project Structure
```text
.
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI server entrypoint
│   ├── rag.py                 # RAG retrieval logic
│   ├── vectorstore.py         # ChromaDB vector index
│   ├── embed.py               # ONNX embedding functions
│   ├── chunking.py            # Sentence-preserving chunking
│   ├── records.py             # SEBI record loader
│   ├── smart_search.py        # TF-IDF lexical search
│   ├── education_guard.py     # Advice refusal guardrail
│   ├── graph.py               # LangGraph workflow
│   ├── agent_loop.py          # Intent routing
│   ├── tools.py               # SIP calculation tools
│   ├── llm.py                 # Groq / Gemini client wrapper
│   ├── cache.py               # In-memory TTL cache
│   ├── observability.py       # Latency logging middleware
│   ├── models.py              # Pydantic schemas
│   └── feedback_store.py      # Local feedback logging
├── ui/
│   └── app.py                 # Streamlit chat interface
├── data/
│   └── records.json           # SEBI knowledge records
├── prompts/
│   ├── system_prompt.txt      # System instructions
│   └── task_prompt_v2.txt     # Task formatting template
├── Dockerfile                 # Lightweight production Dockerfile
├── render.yaml                # Render deployment configuration
└── requirements.txt           # Production dependencies
```

## Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Backend
```bash
uvicorn app.main:app --reload --port 8000
```
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Run Streamlit UI
```bash
streamlit run ui/app.py
```
- Frontend UI: http://localhost:8501

## Docker Deployment
```bash
docker build -t fundfacts-api .
docker run -p 8000:8000 fundfacts-api
```
