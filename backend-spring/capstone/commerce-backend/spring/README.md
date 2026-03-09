# commerce-backend Spring

- Status: `verified scaffold`
- Problem scope covered: commerce API skeleton with catalog, cart, and order surfaces
- Commands:
  - `cp .env.example .env`
  - `make run`
  - `make lint`
  - `make test`
  - `make smoke`
  - `docker compose up --build`

- Known gaps:
  - the capstone is intentionally a modular monolith, not a microservice split
  - payment provider integration is mocked
