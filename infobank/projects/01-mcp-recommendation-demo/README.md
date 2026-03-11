# 01 MCP 추천 최적화

이 프로젝트는 인포뱅크 1번 과제를 `추천 시스템을 어떻게 설계하고 개선 증빙까지 남길 것인가`라는 질문으로 다시 푼다.

## 문제

- MCP catalog와 manifest를 어떤 계약으로 고정할 것인가
- baseline selector, reranker, compare, release gate를 어떤 순서로 쌓을 것인가
- 한국어 추천 이유와 운영 콘솔을 어떻게 같은 제품 설명으로 묶을 것인가

자세한 문제 범위는 [`problem/README.md`](./problem/README.md)에서 본다.

## 공식 답

- 공식 제출 답은 [`capstone/v2-submission-polish`](./capstone/v2-submission-polish/README.md)다.
- 이 버전이 registry seed, manifest validation, reranking, compare, compatibility gate, release gate, artifact export를 한 번에 묶는다.
- stage 학습 내용은 [`capstone/README.md`](./capstone/README.md)와 [`docs/stage-catalog.md`](./docs/stage-catalog.md)에서 역추적한다.

## 확장 답

- 제품화 확장 답은 [`capstone/v3-oss-hardening`](./capstone/v3-oss-hardening/README.md)다.
- 로그인, background jobs, audit log, Compose 배포까지 포함한 self-hosted OSS 후보 버전이다.
- 공식 제출 답이 요구한 범위를 넘어선 운영형 hardening은 이 버전에서만 다룬다.

## 검증

- 공식 답 기준 명령은 [`docs/verification-matrix.md`](./docs/verification-matrix.md)에 모아 둔다.
- 빠른 기준 명령:
  - `cd capstone/v2-submission-polish && pnpm install --no-frozen-lockfile`
  - `pnpm db:up`
  - `pnpm migrate`
  - `pnpm seed`
  - `pnpm test`
  - `pnpm eval`
  - `pnpm compatibility rc-release-check-bot-1-5-0`
  - `pnpm release:gate rc-release-check-bot-1-5-0`

## 읽는 순서

1. [`problem/README.md`](./problem/README.md)
2. [`capstone/README.md`](./capstone/README.md)
3. [`capstone/v2-submission-polish/README.md`](./capstone/v2-submission-polish/README.md)
4. [`docs/stage-catalog.md`](./docs/stage-catalog.md)
5. 필요하면 `stages/00~07`
6. 제품화 방향이 궁금하면 [`capstone/v3-oss-hardening/README.md`](./capstone/v3-oss-hardening/README.md)

## 현재 한계

- 공식 답은 submission 중심이라 production multi-tenant 운영을 목표로 하지 않는다.
- `v3`도 학습용 self-hosted 후보이지 production 보증 버전은 아니다.
- stage 문서는 implementation detail보다 학습 포인트와 증빙 경로를 우선한다.
