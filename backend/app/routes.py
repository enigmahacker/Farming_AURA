from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .models import UserCreate, FarmCreate, WeatherPoint, CropRecommendation, AssistantRequest, AssistantResponse
from .assistant import ask_assistant
from . import knowledge
import time
import os

router = APIRouter()

# Simple in-memory stores for prototype
_USERS = {}
_FARMS = {}
_CROPS_DB = [
    {"crop": "Wheat", "preferred_soil": ["loam", "clay"], "cycle_days": 120, "water_l_per_day": 5.0},
    {"crop": "Maize", "preferred_soil": ["loam", "sandy"], "cycle_days": 100, "water_l_per_day": 6.0},
    {"crop": "Rice", "preferred_soil": ["clay"], "cycle_days": 140, "water_l_per_day": 10.0},
    {"crop": "Millet", "preferred_soil": ["sandy", "loam"], "cycle_days": 90, "water_l_per_day": 3.0},
    {"crop": "Soybean", "preferred_soil": ["loam"], "cycle_days": 110, "water_l_per_day": 4.0},
]


@router.post("/users", status_code=201)
def create_user(payload: UserCreate):
    user_id = int(time.time() * 1000) % (10**8)
    _USERS[user_id] = payload.dict()
    _USERS[user_id]["id"] = user_id
    return {"id": user_id, "user": _USERS[user_id]}


@router.post("/farms", status_code=201)
def create_farm(payload: FarmCreate):
    farm_id = int(time.time() * 1000) % (10**8)
    _FARMS[farm_id] = payload.dict()
    _FARMS[farm_id]["id"] = farm_id
    return {"id": farm_id, "farm": _FARMS[farm_id]}


@router.get("/crops/sample", response_model=List[dict])
def list_sample_crops():
    return _CROPS_DB


def _score_crop(crop_entry, soil_type: str, forecast: dict):
    score = 50.0
    if soil_type and soil_type.lower() in [s.lower() for s in crop_entry.get("preferred_soil", [])]:
        score += 30
    # prefer drier crops if long rain in forecast
    rain_sum = 0.0
    for h in forecast.get("hourly", []):
        rain_sum += h.get("rain_mm", 0.0)
    if rain_sum > 10:
        # reduce score for water intensive crops
        score -= min(20, (crop_entry.get("water_l_per_day", 0) - 4))
    return max(0, score)


@router.post("/recommendations", response_model=List[CropRecommendation])
def recommend_crops(state: str = "", district: str = "", soil_type: str = None, season: str = "kharif", forecast: dict = {}):
    """Return top 5 crop recommendations using rule-based logic.

    For prototype the forecast is a simple dict with hourly rainfall values (list of dicts with 'rain_mm').
    """
    if not soil_type:
        soil_type = "loam"
    scored = []
    for c in _CROPS_DB:
        s = _score_crop(c, soil_type, forecast)
        scored.append({"crop": c["crop"], "score": s, "cycle_days": c.get("cycle_days"), "water_l": c.get("water_l_per_day")})
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)[:5]
    out = []
    for s in scored:
        out.append(CropRecommendation(
            crop=s["crop"],
            suitability_score=round(s["score"]/100.0*5.0, 2),
            expected_yield_increase_pct=round((s["score"]/100.0)*10, 1),
            estimated_water_l_per_day=s.get("water_l"),
            cycle_days=s.get("cycle_days")
        ))
    return out


@router.post("/assistant", response_model=AssistantResponse)
async def assistant(req: AssistantRequest):
    """Simple assistant endpoint. If OPENAI_API_KEY set, it'll forward the request to the configured model.

    Otherwise returns a simple rule-based reply.
    """
    reply = await ask_assistant(req.dict())
    return AssistantResponse(reply=reply, source="ai" if reply else "fallback")


@router.post("/assistant/train")
def assistant_train(payload: dict):
    """Train the assistant by loading JSON documents into the knowledge index.

    Payload example:
    {
      "documents": [ {"id":"1","title":"कपास","text":"...","lang":"hi"}, ... ]
    }
    """
    docs = payload.get("documents") or []
    if not docs:
        return {"added": 0, "message": "Provide key 'documents' with list of docs."}
    added = knowledge.load_from_dicts(docs)
    return {"added": added}


@router.post("/assistant/train_from_file")
def assistant_train_file(payload: dict):
    """Load a JSON file present on the server side under `backend/data/knowledge/`.

    Payload example: { "path": "sample_hindi.json" }
    """
    path = payload.get("path")
    if not path:
        raise HTTPException(status_code=400, detail="Provide 'path' field")
    base = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge")
    full = os.path.normpath(os.path.join(base, path))
    # basic safety check: ensure full starts with base
    if not full.startswith(os.path.normpath(base)):
        raise HTTPException(status_code=400, detail="Invalid path")
    added = knowledge.load_from_file(full)
    return {"added": added, "path": full}


@router.post("/assistant/clear_knowledge")
def assistant_clear():
    knowledge.clear_index()
    return {"cleared": True}
