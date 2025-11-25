# Backend — Farming_AURA (FastAPI prototype)

This folder contains a minimal FastAPI prototype demonstrating:

- Pydantic models for users and farms
- Weather endpoint (mock / blueprint to connect to OpenWeather/Weatherbit)
- Crop recommendation endpoint (rule-based example)
- AI assistant endpoint to proxy to OpenAI (optional)

Quick start (local, Python 3.11+):

1. Create a virtualenv and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set keys (optional)

3. Start the app

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for interactive API docs.

Notes:
- The weather endpoint uses a simple adapter pattern and contains comments to plug in a real weather provider (OpenWeather, Weatherbit).
- The assistant endpoint will call OpenAI if `OPENAI_API_KEY` is set; otherwise it returns a canned response.

Knowledge training and assistant:
- You can train the assistant by posting JSON documents to `/api/assistant/train` or by loading a server-side file with `/api/assistant/train_from_file`.

Example: load the included sample Hindi knowledge file:

```bash
curl -X POST http://localhost:8000/api/assistant/train_from_file -H "Content-Type: application/json" -d '{"path":"sample_hindi.json"}'
```

After training (loading) knowledge, ask the assistant. If `OPENAI_API_KEY` is set, replies will be generated in Hindi using the retrieved knowledge; otherwise a Hindi-friendly fallback composed from matched snippets will be returned.

