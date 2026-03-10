# 08-capstone-submission 문제 정의

## 이 stage가 푸는 문제

v0 runnable snapshot, v1 hardening, v2 improvement proof를 묶은 최종 QA Ops capstone 아카이브다.

## 성공 기준

- v0, v1, v2가 각자 독립적으로 runnable하고 역할이 다르다.
- compare는 같은 dataset과 run label 위에서 baseline 대비 개선을 증빙한다.
- fallback, dependency health, dashboard, proof artifact가 공개 저장소 기준으로 재현 가능하다.

## 왜 지금 이 단계를 먼저 보는가

- 이 항목 자체가 최종 제출물이다.
- tracked docs는 stable index 역할을 하고, notion은 process-heavy technical notebook 역할을 한다.

## 먼저 알고 있으면 좋은 것

- Python 3.12 환경과 `uv`, `pnpm`, Docker가 있으면 검증을 재현하기 쉽다.
- live Upstage/OpenAI/Langfuse 자격증명이 없어도 mock/no-op 경로로 테스트는 가능하다.

## 확인할 증거

- `08-capstone-submission/docs/release-readiness.md`에 실제 실행 명령과 결과가 정리되어 있다.
- `v2-submission-polish/docs/demo/proof-artifacts` 아래에 compare/output artifacts가 저장되어 있다.

## 아직 남아 있는 불확실성

live Upstage/OpenAI/Langfuse 호출은 이 저장소에서 기본 검증 경로에 포함하지 않았다. 현재 증빙은 mock/no-op와 local fallback을 기준으로 한다.
