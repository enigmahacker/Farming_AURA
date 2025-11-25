from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class UserCreate(BaseModel):
    name: str
    phone: Optional[str]
    language: Optional[str] = "hi"


class FarmCreate(BaseModel):
    name: str
    state: str
    district: str
    village: Optional[str] = None
    owner_id: Optional[int] = None
    soil_type: Optional[str] = Field(None, description="sandy/loam/clay/peat")
    land_size_acres: Optional[float] = None
    irrigation_method: Optional[str] = Field(None, description="drip/sprinkler/flood/manual")
    current_crops: Optional[List[str]] = []


class WeatherPoint(BaseModel):
    timestamp: int
    temp_c: float
    humidity: float
    rain_mm: Optional[float] = 0.0
    wind_kph: Optional[float] = 0.0


class CropRecommendation(BaseModel):
    crop: str
    suitability_score: float
    expected_yield_increase_pct: Optional[float]
    estimated_water_l_per_day: Optional[float]
    cycle_days: Optional[int]


class AssistantRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    context: Optional[dict] = None


class AssistantResponse(BaseModel):
    reply: str
    source: Optional[str] = "cached"
