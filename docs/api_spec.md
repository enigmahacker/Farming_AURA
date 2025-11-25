# API Specification (prototype)

Base path: `/api`

Endpoints:

- `GET /health` — basic health

- `POST /api/users` — create user
  - body: `{ name, phone?, language? }`
  - response: `{ id, user }`

- `POST /api/farms` — create farm profile
  - body: `{ owner_id?, name, state, district, village?, soil_type?, land_size_acres?, irrigation_method?, current_crops? }`
  - response: `{ id, farm }`

- `GET /api/crops/sample` — list sample crop rows used by recommender

- `POST /api/recommendations` — rule-based crop recommendations
  - query args or body: `state`, `district`, `soil_type`, `season`, `forecast` (forecast is optional; see model below)
  - response: list of `{ crop, suitability_score (1-5), expected_yield_increase_pct, estimated_water_l_per_day, cycle_days }`

- `POST /api/assistant` — AI assistant
  - body: `{ user_id?, message, context? }`
  - response: `{ reply, source }`

Models used by the API are included as Pydantic classes in `backend/app/models.py` and appear in the interactive Swagger UI when the server runs.
