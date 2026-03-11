# 02 챗봇 상담 품질 관리 문제 정의

## 원래 과제가 묻는 것

- 상담 챗봇 답변 품질을 어떤 기준으로 평가할 것인가
- rule/guardrail, evidence verification, judge scoring, regression proof를 어떤 구조로 묶을 것인가
- 운영자가 실패 사례와 개선 증빙을 콘솔에서 재검토할 수 있게 만들 수 있는가

## 이 레포의 공식 답

- 공식 답은 `projects/02-chat-qa-ops/capstone/v2-submission-polish`다.
- 이 버전은 rubric, guardrail, evidence pipeline, compare proof, submission artifact를 하나의 제출형 답으로 묶는다.
- `stages/00~07`은 공식 답을 이루는 계약과 검증 단위를 분리한 학습 pack이다.

## 제공 자료와 기준

- 전역 커리큘럼 근거: `docs/curriculum/project-selection-rationale.md`
- 전역 순서표: `docs/curriculum/curriculum-map.md`
- 레퍼런스 뼈대: `docs/curriculum/reference-spine.md`

## 범위 밖

- production BPO 운영
- real customer PII 처리
- multi-tenant SaaS, SSO, billing

## canonical verify

```bash
cd projects/02-chat-qa-ops/capstone/v2-submission-polish/python
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
UV_PYTHON=python3.12 make smoke-postgres
```
