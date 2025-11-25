import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_user():
    response = client.post("/api/users", json={
        "name": "राज कुमार",
        "phone": "9876543210",
        "language": "hi"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["user"]["name"] == "राज कुमार"


def test_create_farm():
    response = client.post("/api/farms", json={
        "name": "खेत 1",
        "state": "उत्तर प्रदेश",
        "district": "लखनऊ",
        "soil_type": "loam",
        "land_size_acres": 2.5,
        "irrigation_method": "drip"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["farm"]["district"] == "लखनऊ"


def test_get_sample_crops():
    response = client.get("/api/crops/sample")
    assert response.status_code == 200
    crops = response.json()
    assert len(crops) > 0
    assert "crop" in crops[0]


def test_recommendations():
    response = client.post("/api/recommendations", json={
        "state": "UP",
        "district": "Lucknow",
        "soil_type": "loam",
        "season": "rabi",
        "forecast": {"hourly": [{"rain_mm": 0}]}
    })
    assert response.status_code == 200
    recs = response.json()
    assert len(recs) > 0
    assert "crop" in recs[0]
    assert "suitability_score" in recs[0]


def test_assistant_fallback():
    # Test without knowledge loaded
    response = client.post("/api/assistant", json={
        "message": "कृपया सलाह दें"
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data


def test_assistant_train():
    docs = [
        {
            "id": "test_1",
            "title": "टेस्ट",
            "text": "यह एक परीक्षण दस्तावेज़ है।",
            "lang": "hi"
        }
    ]
    response = client.post("/api/assistant/train", json={
        "documents": docs
    })
    assert response.status_code == 200
    assert response.json()["added"] == 1


def test_assistant_train_from_file():
    response = client.post("/api/assistant/train_from_file", json={
        "path": "sample_hindi.json"
    })
    assert response.status_code == 200
    assert response.json()["added"] > 0


def test_assistant_with_knowledge():
    # Clear and train with fresh knowledge
    client.post("/api/assistant/clear_knowledge")
    client.post("/api/assistant/train", json={
        "documents": [
            {
                "id": "wheat_test",
                "title": "गेहूं",
                "text": "गेहूं अक्टूबर में बोएं।",
                "lang": "hi"
            }
        ]
    })
    # Now ask
    response = client.post("/api/assistant", json={
        "message": "गेहूं कब बोएं?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0


def test_assistant_clear():
    response = client.post("/api/assistant/clear_knowledge")
    assert response.status_code == 200
    assert response.json()["cleared"] is True
