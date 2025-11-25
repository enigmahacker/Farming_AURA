# Setup and Quickstart Guide

This document provides complete instructions to set up, run, test, and develop the Farming_AURA application locally.

## Prerequisites

- Python 3.10+ or Docker
- Git
- Virtual environment (recommended)

## 1. Local Setup (Python venv)

### Step 1: Clone and navigate

```bash
cd /workspaces/Farming_AURA
```

### Step 2: Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
pip install pytest pytest-asyncio  # For testing
```

### Step 3: Copy environment file

```bash
cp backend/.env.example backend/.env
# Edit backend/.env to add your API keys (optional for basic testing)
```

### Step 4: Run backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 2. Docker Setup (Optional)

```bash
# From repo root
docker compose up --build
```

The backend will run on http://localhost:8000

## 3. Running Tests

```bash
cd backend
pytest tests/ -v
```

All 10 tests should pass:
- Health check
- User creation
- Farm creation
- Sample crops
- Crop recommendations
- Assistant (with/without knowledge)
- Knowledge training endpoints
- Knowledge clearing

## 4. Using the API

### 4.1 Create a User

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"राज कुमार","phone":"9876543210","language":"hi"}'
```

Response:
```json
{
  "id": 1234567890,
  "user": {
    "name": "राज कुमार",
    "phone": "9876543210",
    "language": "hi",
    "id": 1234567890
  }
}
```

### 4.2 Create a Farm

```bash
curl -X POST http://localhost:8000/api/farms \
  -H "Content-Type: application/json" \
  -d '{
    "name":"मेरा खेत",
    "state":"उत्तर प्रदेश",
    "district":"लखनऊ",
    "soil_type":"loam",
    "land_size_acres":2.5,
    "irrigation_method":"drip"
  }'
```

### 4.3 Get Crop Recommendations

```bash
curl -X POST 'http://localhost:8000/api/recommendations' \
  -H "Content-Type: application/json" \
  -d '{"state":"UP","district":"Lucknow","soil_type":"loam","season":"rabi"}'
```

### 4.4 Train Assistant with Knowledge

First, load the included Hindi knowledge:

```bash
curl -X POST http://localhost:8000/api/assistant/train_from_file \
  -H "Content-Type: application/json" \
  -d '{"path":"sample_hindi.json"}'
```

Or post custom documents:

```bash
curl -X POST http://localhost:8000/api/assistant/train \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "fert_1",
        "title": "नाइट्रोजन उर्वरक",
        "text": "नाइट्रोजन पत्तियों के विकास के लिए आवश्यक है...",
        "lang": "hi"
      }
    ]
  }'
```

### 4.5 Ask the Assistant

```bash
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"message":"गेहूं कब बोना चाहिए?"}'
```

**With OpenAI**: If you set `OPENAI_API_KEY` in `.env`, the assistant will generate natural Hindi responses using OpenAI's GPT model.

**Without OpenAI**: The assistant returns matched knowledge snippets or Hindi fallback messages.

## 5. Architecture Overview

### Backend (FastAPI)

- **Main**: `/backend/app/main.py` — FastAPI app initialization
- **Routes**: `/backend/app/routes.py` — all API endpoints
- **Models**: `/backend/app/models.py` — Pydantic request/response schemas
- **Assistant**: `/backend/app/assistant.py` — AI assistant logic with knowledge retrieval
- **Knowledge**: `/backend/app/knowledge.py` — JSON document loader and keyword-based retriever
- **Data**: `/backend/data/knowledge/` — sample Hindi knowledge JSON files
- **Tests**: `/backend/tests/test_api.py` — comprehensive test suite

### Frontend (Notes)

- Design philosophy: big fonts, icons, Hindi-first, farmer-friendly
- 8 key screens: Splash, Dashboard, Weather, Crop Recommendations, Watering Schedule, Alerts, Knowledge Hub, Settings
- Build with Flutter or React Native (scaffolding and screen mockups in `/frontend/`)

### Documentation

- `/docs/api_spec.md` — endpoint reference and payload examples
- `/docs/data_model.md` — data entities, schemas, production DB recommendations
- `/README.md` — project overview

## 6. Extending the System

### 6.1 Add More Knowledge

Create a new JSON file in `/backend/data/knowledge/`:

```json
[
  {
    "id": "pest_001",
    "title": "गिड़ी (Thrips) नियंत्रण",
    "text": "गिड़ी छोटे कीट हैं जो पत्तियों को पीली करते हैं। नीम का तेल या कीटनाशक स्प्रे करें।",
    "lang": "hi"
  }
]
```

Load it via:
```bash
curl -X POST http://localhost:8000/api/assistant/train_from_file \
  -H "Content-Type: application/json" \
  -d '{"path":"pest_control.json"}'
```

### 6.2 Integrate a Real Weather API

In `/backend/app/routes.py`, add a weather endpoint that calls OpenWeather or Weatherbit:

```python
@router.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    # Call OpenWeather API and return formatted response
    pass
```

### 6.3 Add Database (Postgres)

Replace in-memory stores in `/backend/app/routes.py` with SQLAlchemy models and queries.

### 6.4 Improve Knowledge Retrieval

Replace keyword-based retrieval in `/backend/app/knowledge.py` with:
- Sentence-Transformers embeddings
- FAISS or Annoy for approximate nearest neighbor search
- Metadata filtering by crop, season, state

## 7. Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Ensure venv is activated and dependencies installed: `pip install -r backend/requirements.txt`

**Issue**: Port 8000 already in use
- **Solution**: Run on a different port: `uvicorn app.main:app --port 8001`

**Issue**: Tests fail with 422 status
- **Solution**: Check Pydantic model definitions; ensure all required fields have defaults in test payloads.

**Issue**: Assistant returns fallback response (not OpenAI)
- **Solution**: Set `OPENAI_API_KEY` in `.env` file: `OPENAI_API_KEY=sk-...`

## 8. Next Steps

1. **Frontend**: Build Flutter/React Native app using `/frontend/README.md` as a reference and connect to the backend API.
2. **Mobile screens**: Implement Home Dashboard, Weather Forecast, Crop Recommendations, etc.
3. **Knowledge base**: Add comprehensive Hindi content (crop guides, pest control, fertilizer schedules).
4. **ML model**: Train a crop recommendation model using location, soil, weather, and historical data.
5. **Notifications**: Add SMS alerts (Twilio/Msg91) and push notifications.
6. **Offline mode**: Cache weather and knowledge locally on mobile devices.

---

**Questions?** Check the code comments and docstrings in the `backend/app/` files, or refer to the FastAPI documentation: https://fastapi.tiangolo.com/

