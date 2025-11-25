# Data Model (Developer notes)

This document describes the primary entities for the Farming_AURA prototype and recommended schema for production.

Entities:

- User
  - `id` (pk)
  - `name`
  - `phone`
  - `language` (hi/en)
  - `created_at`

- Farm
  - `id` (pk)
  - `owner_id` (fk -> user.id)
  - `name`
  - `state`
  - `district`
  - `village`
  - `soil_type`
  - `land_size_acres`
  - `irrigation_method`
  - `current_crops` (array)

- WeatherLog
  - `id`
  - `farm_id`
  - `timestamp`
  - `temp_c`
  - `humidity`
  - `rain_mm`
  - `wind_kph`
  - `uv_index`

- Crop
  - `id`
  - `name`
  - `preferred_soil` (array)
  - `cycle_days`
  - `water_l_per_day`
  - `seasonality` (rabi/kharif/zaid)

- Alert
  - `id`
  - `farm_id`
  - `type` (weather/watering/pest)
  - `level` (green/yellow/red)
  - `message`
  - `created_at`

Recommended production DB choices:

- Relational store (Postgres) for core entities
- Time-series or cache store (InfluxDB/Redis) for weather time-series and derived aggregates
- Messaging queue (RabbitMQ or AWS SQS) for alert dispatch

Indexes & performance:

- Index `weatherlog(farm_id, timestamp)` for range queries
- Index `farm(state, district)` to fetch farms by location for regional advice
