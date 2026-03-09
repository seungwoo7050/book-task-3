# B-federation-security-lab Spring

- Status: `verified scaffold`
- Problem scope covered: Google OAuth2 callback modeling, 2FA flows, audit log surface
- Commands:
  - `cp .env.example .env`
  - `make run`
  - `make lint`
  - `make test`
  - `make smoke`
  - `docker compose up --build`

- Known gaps:
  - Google integration is simulated rather than tied to a real console app
  - TOTP generation is simplified for study readability
