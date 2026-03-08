# Reference Spine

## 메인 교과서

### 1. AI Engineering

- URL: https://huyenchip.com/books/
- 역할
  - LLM 애플리케이션 수명주기
  - evaluation, iteration, observability
  - 실험에서 운영으로 넘어가는 관점

### 2. Designing Machine Learning Systems

- URL: https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/
- 역할
  - 문제 정의와 시스템 경계 설정
  - 데이터/피드백 루프
  - 모니터링과 운영 설계 원칙

## 실전 레퍼런스

### Ragas

- URL: https://docs.ragas.io/
- 용도
  - faithfulness, groundedness, retrieval 관점
  - evaluation dataset과 실험 루프 설계

### Langfuse

- URL: https://langfuse.com/
- 용도
  - traces, datasets, evals, 운영 지표
  - UI와 관측성 레이어 참고

## 트랙별 핵심 구현 레퍼런스

### study1: MCP Recommendation Ops

- MCP TypeScript SDK
  - URL: https://modelcontextprotocol.io/docs/sdk
  - 이유
    - registry, manifest, compatibility 흐름이 공식 SDK 기준으로 설명 가능해야 한다.
- MCP Registry
  - URL: https://registry.modelcontextprotocol.io/
  - 이유
    - catalog, metadata, versioning, ecosystem norms를 확인하는 기준면이다.
- Changesets
  - URL: https://github.com/changesets/changesets
  - 이유
    - semver, release note, version gate 설계를 현실적인 배포 흐름에 맞춘다.

### study2: Chat QA Ops

- FastAPI
  - URL: https://fastapi.tiangolo.com/
  - 이유
    - evaluation API, operator tooling, typed backend를 빠르게 묶을 수 있다.
- Upstage Solar
  - URL: https://www.upstage.ai/products/solar-pro
  - 이유
    - 한국어 상담 평가와 한국 기업 도입 설명에 유리한 1순위 모델 어댑터다.
- Langfuse
  - URL: https://langfuse.com/
  - 이유
    - trace, eval, dataset, experiment lineage를 운영형으로 설명할 수 있다.

### study3: Voice Meeting Assistant

- NAVER Cloud CLOVA Speech
  - URL: https://guide.ncloud-docs.com/docs/clovaspeech-overview
  - 이유
    - 한국어 회의 STT 품질과 국내 시장 적합성을 설명하는 주력 선택지다.
- CLOVA Speech Recognition Spec
  - URL: https://guide.ncloud-docs.com/docs/en/csr-spec
  - 이유
    - 장시간 단일 호출이 아니라 rolling chunk 파이프라인을 선택해야 하는 근거다.
- OpenAI Realtime / Responses
  - URL: https://platform.openai.com/docs/guides/realtime
  - 이유
    - 개입 타이밍 이후 action generation과 low-latency reasoning 데모에 적합하다.

## 선택적 참고

### DeepEval

- 이번 레포에서는 메인 교재가 아니다.
- 이유
  - 현재 공식 메시지가 범용 평가 라이브러리보다는 보안/리스크 평가 플랫폼 쪽으로 이동해 있다.
  - 평가 관점 참고는 가능하지만 커리큘럼의 기준축으로 고정하기에는 불안정하다.

## 스택 기본값

- 공통 기본값
  - `AWS Seoul`을 기본 운영 설명으로 둔다.
  - 외부 서비스 의존 기능은 모두 `mock` 또는 `replay` fallback을 기본 제공한다.
  - 제출 시연은 5분 안에 핵심 가치가 보이도록 runbook과 proof artifact를 함께 둔다.
- study1
  - `TypeScript + Node.js + Fastify + Zod`
  - `Next.js + React`
  - `PostgreSQL`
  - `pnpm + Changesets + GitHub Actions`
  - `Vitest + Playwright`
- study2
  - `Python 3.12 + FastAPI + Pydantic + SQLAlchemy`
  - `React + Vite`
  - `PostgreSQL`
  - `Langfuse`
  - `Upstage Solar` primary, `OpenAI` secondary, `Ollama` fallback
- study3
  - `TypeScript + Node.js + Fastify + WebSocket`
  - `Next.js + React`
  - `NAVER Cloud CLOVA Speech`
  - `OpenAI Realtime or Responses API`
  - `PostgreSQL`
  - `Vitest + Playwright`

LLM 의존 기능은 모두 mock 또는 heuristic fallback을 기본 제공해야 한다.
