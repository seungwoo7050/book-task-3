# Chat QA Ops Verification Matrix

| 대상 | 목적 | 명령 |
| --- | --- | --- |
| `capstone/v2-submission-polish/python` | 공식 제출 답 dev toolchain 준비 | `UV_PYTHON=python3.12 uv sync --extra dev` |
| `capstone/v2-submission-polish/python` | 공식 제출 답 전체 gate | `UV_PYTHON=python3.12 make gate-all` |
| `capstone/v2-submission-polish/python` | PostgreSQL smoke path | `UV_PYTHON=python3.12 make smoke-postgres` |
| `capstone/v3-self-hosted-oss/python` | 확장 버전 gate | `UV_PYTHON=python3.12 make gate-all` |
| `capstone/v3-self-hosted-oss/react` | 확장 버전 UI 회귀 | `pnpm test --run` |
| `stages/04-claim-and-evidence-pipeline/python` | 대표 stage 검증 | `UV_PYTHON=python3.12 uv run pytest -q` |
