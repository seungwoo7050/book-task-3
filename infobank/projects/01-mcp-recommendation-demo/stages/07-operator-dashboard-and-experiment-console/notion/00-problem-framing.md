# 07 운영자 대시보드와 실험 콘솔 문제 정의

## 이 stage가 맡는 문제

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 정리해 추천 시스템의 운영 면을 보여 주는 단계다.

## 현재 기준 성공 조건

- 추천 시스템이 단일 API가 아니라 운영 도구까지 포함한다는 점을 보여 준다.
- 학생이 자기 포트폴리오에서 운영자 UI를 어떻게 설명할지 참고할 수 있다.
- 최종 capstone의 화면 중심 시연 경로가 명확해진다.

## 먼저 알고 있으면 좋은 것

- 상위 `README.md`, `problem/README.md`, `docs/README.md`를 먼저 읽어 stage 목적을 고정한다.
- 실제 구현 확인은 `v2-submission-polish` 기준으로 내려가야 한다.
- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.

## 확인할 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`

## 아직 남아 있는 불확실성

- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.
