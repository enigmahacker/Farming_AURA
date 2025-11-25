# Farming_AURA — Smart Farming Weather & Crop Advisor

A complete, developer-ready scaffold for an AI-powered farming advisory app. Built with **FastAPI** backend, **Flutter** frontend guidance, and **Hindi-first** AI assistant.

## 🚀 Quick Start

```bash
# Option 1: Local Python
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Open http://localhost:8000/docs

# Option 2: Docker
docker compose up --build
```

All 10 API tests pass ✅. See `SETUP.md` for detailed instructions.

## 📦 What's Included

| Component | Status | Location |
|-----------|--------|----------|
| **Backend** | ✅ Working | `backend/` — FastAPI with 8+ endpoints, Pydantic models, rule-based crop recommender, AI assistant |
| **AI Assistant** | ✅ Working | `backend/app/assistant.py` — JSON knowledge training, Hindi support, OpenAI integration (optional) |
| **Data Models** | ✅ Complete | `docs/data_model.md` — Users, Farms, Weather, Crops, Alerts, Recommendations |
| **API Spec** | ✅ Complete | `docs/api_spec.md` — Full endpoint reference with examples |
| **Tests** | ✅ 10/10 Passing | `backend/tests/test_api.py` — Comprehensive coverage |
| **Frontend Guide** | ✅ Complete | `frontend/README.md` — UI/UX plan, 8 key screens, Flutter example |
| **Setup Docs** | ✅ Complete | `SETUP.md` — Installation, API examples, troubleshooting |
| **Roadmap** | ✅ Complete | `ROADMAP.md` — Production phases, feature status, next steps |

## 🎯 Features

### Backend API
- ✅ User onboarding (language, location, farm profile)
- ✅ Crop recommendations (rule-based, top 5 matches)
- ✅ AI assistant with JSON knowledge training
- ✅ Hindi-first responses with fallback
- ✅ Weather monitoring (blueprint)
- ✅ Alert system (data model ready)

### AI Chatbot
- ✅ Train on custom JSON knowledge
- ✅ Keyword-based retrieval (prototype)
- ✅ Hindi language support
- ✅ OpenAI integration (optional; fallback when key not set)
- ✅ Sample Hindi knowledge included

### Frontend
- ✅ 8 key screen designs (Dashboard, Weather, Crops, Watering, Alerts, Knowledge, Settings)
- ✅ Flutter example with API integration
- ✅ Farmer-friendly design (big fonts, icons, high contrast)
- ✅ Earthy color palette (greens, browns, blues)

### Developer Tools
- ✅ Docker & docker-compose
- ✅ Python venv setup
- ✅ Comprehensive test suite
- ✅ API documentation (Swagger + ReDoc)

## 📚 Documentation

- **Getting Started**: See [`SETUP.md`](SETUP.md) for full setup & API examples
- **Implementation Details**: Read [`ROADMAP.md`](ROADMAP.md) for architecture, phases, success metrics
- **API Reference**: Check [`docs/api_spec.md`](docs/api_spec.md)
- **Data Model**: Review [`docs/data_model.md`](docs/data_model.md)
- **Frontend**: See [`frontend/README.md`](frontend/README.md)
- **Backend**: Read [`backend/README.md`](backend/README.md)

## 💻 API Examples

### Train the Assistant with Hindi Knowledge
```bash
curl -X POST http://localhost:8000/api/assistant/train_from_file \
  -H "Content-Type: application/json" \
  -d '{"path":"sample_hindi.json"}'
```

### Ask the Assistant
```bash
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"message":"गेहूं कब बोना चाहिए?"}'
```

### Get Crop Recommendations
```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"state":"UP","district":"Lucknow","soil_type":"loam","season":"rabi"}'
```

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
# All 10 tests pass ✅
```

## 🗺️ Project Structure

```
backend/
  ├── app/
  │   ├── main.py           # FastAPI app
  │   ├── routes.py         # Endpoints
  │   ├── models.py         # Pydantic schemas
  │   ├── assistant.py      # AI + knowledge retrieval
  │   └── knowledge.py      # JSON loader
  ├── data/knowledge/
  │   └── sample_hindi.json # Sample Hindi knowledge
  ├── tests/test_api.py     # 10 tests
  └── requirements.txt

frontend/
  ├── README.md             # UI/UX plan
  └── example_home_screen.dart  # Flutter example

docs/
  ├── api_spec.md           # API reference
  └── data_model.md         # Database schema

SETUP.md                     # Complete setup guide
ROADMAP.md                   # Phases & production plan
```

## 🎨 Design Philosophy

- **Big Fonts**: 20-24px headings, 14-16px body (accessible to elders)
- **Icons Everywhere**: Visual cues for actions
- **Hindi-First**: UI in Hindi with English fallback
- **High Contrast**: Easy to read in sunlight
- **Offline-Ready**: Works without internet
- **Minimal Clutter**: Focus on essentials only
- **Earthy Colors**: Greens (#2D5016), browns, blues

## 🔄 Next Steps

1. **Local Development**: Follow `SETUP.md` to run the backend locally
2. **API Exploration**: Open http://localhost:8000/docs to try endpoints
3. **Knowledge Training**: Add your own Hindi knowledge via `/api/assistant/train`
4. **Frontend Build**: Use `frontend/example_home_screen.dart` as starting point
5. **Deployment**: See `ROADMAP.md` for production checklist

## 📊 Development Status

| Phase | Status |
|-------|--------|
| Backend Prototype | ✅ Complete |
| AI Assistant | ✅ Complete |
| API Testing | ✅ 10/10 Passing |
| Frontend Guide | ✅ Complete |
| Documentation | ✅ Complete |
| **Next: Production Setup** | 🟡 Ready |

## 🤝 Contributing

- Fork & create feature branch
- Add tests for new features
- Run `pytest tests/` before submitting PR
- Update docs if needed

## 📞 Support

- Read `SETUP.md` for detailed instructions
- Check `ROADMAP.md` for architecture & roadmap
- Open GitHub issues for bugs
- See inline code comments for implementation details

## 📜 License

MIT — Free to use and modify

---

**Built with ❤️ for Indian Farmers**

Farming_AURA brings modern AI to rural agriculture through local knowledge, real-time guidance, and accessible technology.