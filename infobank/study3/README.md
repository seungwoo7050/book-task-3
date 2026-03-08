# Study 3

주제는 음성 회의 어시스턴트다.
최종 목표는 한국어 회의를 실시간에 가깝게 캡처하고, 토픽 전환과 쟁점을 구조화하고, 적절한 시점에 개입 액션과 지원 자료를 제시하는 회의 지원 데모다.

## Primary Stack

- `TypeScript + Node.js + Fastify + WebSocket`
- `Next.js + React`
- STT: `NAVER Cloud CLOVA Speech`
- 개입/추론: `OpenAI Realtime or Responses API`
- `PostgreSQL`
- `Vitest + Playwright`
- 배포/운영 기본 설명: `AWS Seoul`

## Capstone Policy

- `08-capstone-submission/v0-initial-demo`: 최초 제출 가능한 데모
- `08-capstone-submission/v1-live-intervention`: `v0` 복제 후 실시간 개입 정책 강화
- `08-capstone-submission/v2-submission-polish`: `v1` 복제 후 제출 정리

## Sequence

`00-source-brief` -> `01-meeting-event-model-and-success-metrics` -> `02-audio-capture-and-stt-chunk-pipeline` -> `03-topic-shift-detection-and-issue-graph` -> `04-intervention-timing-and-action-policy` -> `05-material-retrieval-analysis-and-sharing` -> `06-scenario-regression-and-safety-gates` -> `07-operator-console-and-replay-viewer` -> `08-capstone-submission`
