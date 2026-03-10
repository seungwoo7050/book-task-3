# Capstone — 문제 정의

## 풀어야 하는 문제

stage 00~07에서 만든 모듈들은 각각 독립적으로 동작한다.
하지만 실제 상담 QA 운영 시스템은 이 모듈들이 **하나의 파이프라인으로 연결**되어야 한다.

```
데이터 업로드 → retrieval → judge → merge → regression → 대시보드 표시
```

이 연결을 한 번에 완성하면 실패 확률이 높다.
그래서 4단계 버전으로 점진적으로 통합한다.

## 4-version 전략

### v0 — Initial Demo
**목적**: 끝까지 한 번 연결해서 동작하는 것을 보여준다.

- SQLite + 로컬 fallback 중심
- heuristic judge만 사용
- golden set replay 동작
- 4페이지 대시보드 전체 작동

v0의 성공 기준: `make init-db && make seed-demo && make test-backend`이 통과하고, 대시보드에서 데이터가 보이면 된다.

### v1 — Regression Hardening
**목적**: provider chain과 trace 기반 운영 검증 강화.

- Upstage Solar → OpenAI → Ollama provider chain
- golden set 커버리지 확대
- version compare 강화
- Langfuse lineage/trace envelope 준비
- PostgreSQL smoke path + SQLite fallback 정리

v1의 핵심 변화: judge가 더 이상 heuristic 하나가 아니라, 실패 시 다음 provider로 넘어가는 chain이 된다.

### v2 — Submission Polish
**목적**: retrieval 품질 개선을 수치로 증명한다.

- retrieval-v2: alias/category/risk rerank
- retrieval-conditioned safe answer composer
- baseline(v1) vs candidate(v2) compare artifact 생성
- 결과: avg_score 84.06 → 87.76, critical 2→0, pass 16→19, fail 14→11

v2의 핵심 산출물: compare JSON과 improvement report.

### v3 — Self-Hosted OSS
**목적**: 외부 팀이 바로 배포할 수 있는 OSS 패키지.

- 관리자 로그인 (single admin auth)
- transcript JSONL 업로드 + KB bundle ZIP 업로드
- 비동기 evaluation job + worker 처리
- Docker Compose 원커맨드 배포
- optional AI profile (ollama, chroma)

v3의 성공 기준: `docker compose up --build` 한 번으로 전체 시스템이 동작한다.

## 제약

- multi-tenant, RBAC, SSO, billing은 범위 밖
- single admin auth만 지원
- Kubernetes 배포는 고려하지 않음
