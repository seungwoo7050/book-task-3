# 레퍼런스 스파인

이 문서는 각 트랙이 어떤 기준 교재와 공식 문서를 뼈대로 삼는지 정리한 인덱스다. 아래 링크는 2026-03-10 기준으로 공식 페이지 접근 가능 여부를 다시 확인했다.

## 공통 기준 교재

### AI Engineering 교재

- URL: https://huyenchip.com/books/
- 보는 이유
  - LLM 애플리케이션 수명주기와 평가 루프를 큰 그림에서 이해하기 좋다.
  - 아이디어를 데모에서 운영형 시스템으로 옮길 때 필요한 관점을 제공한다.

### Designing Machine Learning Systems 교재

- URL: https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- 보는 이유
  - 문제 정의, 시스템 경계, 피드백 루프, 모니터링 원칙을 정리하기 좋다.

## 공통 실전 참고

### Ragas 공식 문서

- URL: https://docs.ragas.io/
- 쓰는 이유
  - groundedness, retrieval, faithfulness 평가 관점을 정리할 때 기준점으로 삼기 좋다.

### Langfuse 공식 문서

- URL: https://langfuse.com/docs
- 쓰는 이유
  - trace, dataset, eval, experiment lineage 같은 운영형 관측성 개념을 정리할 때 도움이 된다.

## 1번 과제: `projects/01-mcp-recommendation-demo/`

### Model Context Protocol SDK 문서

- URL: https://modelcontextprotocol.io/docs/sdk
- 쓰는 이유
  - manifest, metadata, SDK usage, 호환성 설명을 공식 용어로 맞출 수 있다.

### MCP Registry 기준면

- URL: https://registry.modelcontextprotocol.io/
- 쓰는 이유
  - catalog, versioning, ecosystem 관례를 확인하는 기준면으로 삼는다.

### Changesets 공식 문서

- URL: https://github.com/changesets/changesets
- 쓰는 이유
  - semver, release note, release gate 흐름을 현실적인 배포 관행과 연결하기 좋다.

## 2번 과제: `projects/02-chat-qa-ops/`

### FastAPI 공식 문서

- URL: https://fastapi.tiangolo.com/
- 쓰는 이유
  - 평가 API와 운영 도구용 typed backend를 빠르게 구성하기 좋다.

### Upstage Solar 소개

- URL: https://www.upstage.ai/products/solar-pro
- 쓰는 이유
  - 한국어 상담 평가 시나리오에 어울리는 상용 모델 후보를 설명할 때 기준으로 삼는다.

### Langfuse 공식 문서

- URL: https://langfuse.com/docs
- 쓰는 이유
  - trace, eval, dataset, experiment lineage를 운영형으로 설명하기 좋다.

## 스택 기본값

- 공통
  - 한국어 시나리오와 한국 시장 설명력을 기본값으로 둔다.
  - 외부 서비스 의존 기능은 `mock`, `replay`, `heuristic fallback` 가운데 하나를 반드시 준비한다.
  - 최종 데모는 5분 안에 핵심 가치를 보여 주는 runbook과 proof artifact를 함께 제공한다.
- `projects/01-mcp-recommendation-demo/`
  - `TypeScript + Node.js + Fastify + Zod`
  - `Next.js + React`
  - `PostgreSQL`
  - `pnpm + Changesets + GitHub Actions`
  - `Vitest + Playwright`
- `projects/02-chat-qa-ops/`
  - `Python 3.12 + FastAPI + Pydantic + SQLAlchemy`
  - `React + Vite`
  - `PostgreSQL`
  - `Langfuse`
  - `Upstage Solar` primary, `OpenAI` secondary, `Ollama` fallback
