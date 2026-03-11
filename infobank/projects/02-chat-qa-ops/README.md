# 02 챗봇 상담 품질 관리

이 프로젝트는 인포뱅크 2번 과제를 `상담 품질을 정의하고 자동 평가·회귀·운영 콘솔까지 연결하는 QA Ops 계층`으로 다시 푼다.

## 문제

- 상담 품질을 어떤 rubric과 failure taxonomy로 정의할 것인가
- guardrail, evidence verification, judge scoring, regression compare를 어떤 순서로 합성할 것인가
- 평가 결과와 trace를 운영 콘솔에서 어떻게 읽히게 만들 것인가

자세한 문제 범위는 [`problem/README.md`](./problem/README.md)에서 본다.

## 공식 답

- 공식 제출 답은 [`capstone/v2-submission-polish`](./capstone/v2-submission-polish/README.md)다.
- 이 버전이 평가 파이프라인, golden regression, compare artifact, 제출용 proof를 가장 선명하게 묶는다.
- stage 학습 흐름은 [`capstone/README.md`](./capstone/README.md)와 [`docs/stage-catalog.md`](./docs/stage-catalog.md)로 이어진다.

## 확장 답

- 제품화 확장 답은 [`capstone/v3-self-hosted-oss`](./capstone/v3-self-hosted-oss/README.md)다.
- 로그인, 업로드, 비동기 job, Docker Compose quickstart를 더한 self-hosted OSS 후보 버전이다.
- 공식 제출 답에서 요구한 범위를 넘어선 운영/설치 경험은 여기서만 다룬다.

## 검증

- 공식 답 기준 명령은 [`docs/verification-matrix.md`](./docs/verification-matrix.md)에 모아 둔다.
- 빠른 기준 명령:
  - `cd capstone/v2-submission-polish/python`
  - `UV_PYTHON=python3.12 uv sync --extra dev`
  - `UV_PYTHON=python3.12 make gate-all`
  - `UV_PYTHON=python3.12 make smoke-postgres`

## 읽는 순서

1. [`problem/README.md`](./problem/README.md)
2. [`capstone/README.md`](./capstone/README.md)
3. [`capstone/v2-submission-polish/README.md`](./capstone/v2-submission-polish/README.md)
4. [`docs/stage-catalog.md`](./docs/stage-catalog.md)
5. 필요하면 `stages/00~07`
6. self-hosted 방향이 궁금하면 [`capstone/v3-self-hosted-oss/README.md`](./capstone/v3-self-hosted-oss/README.md)

## 현재 한계

- 공식 답은 submission 중심이라 production 운영 보증을 목표로 하지 않는다.
- `v3`도 single-team self-hosted 참고 버전이지 SaaS 제품 완성본은 아니다.
- stage 문서는 제품 구현보다 학습 근거와 증빙 경로를 우선한다.
