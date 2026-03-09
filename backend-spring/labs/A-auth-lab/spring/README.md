# A-auth-lab Spring

- Status: `verified scaffold`
- Problem scope covered: local account auth surfaces, token rotation modeling, Mailpit-ready local workflow
- Build command:

```bash
cp .env.example .env
make run
```

- Lint command:

```bash
make lint
```

- Test command:

```bash
make test
```

- Smoke command:

```bash
make smoke
```

- Docker command:

```bash
docker compose up --build
```

- Known gaps:
  - auth persistence is intentionally lightweight in the initial scaffold
  - email verification and password reset are modeled API-first without a frontend
