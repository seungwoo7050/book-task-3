# 07 운영자 대시보드와 실험 콘솔

## 이 stage의 문제

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 설계해 추천 시스템의 운영 면을 보여 준다.

## 입력/제약

- 입력: catalog 상태, experiment 메타데이터, release candidate, compare 결과
- 제약: 운영 작업과 실험 결과를 같은 정보 구조에서 읽게 해야 한다.

## 이 stage의 답

- 운영 콘솔 IA를 catalog 관리, 실험 관리, release candidate 관리 축으로 정리한다.
- 실험 결과와 운영 작업이 같은 dashboard narrative 안에 들어가게 만든다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- `v2-submission-polish/tests/e2e/recommendation.spec.ts`를 통해 운영 콘솔 시나리오를 확인한다.

## 현재 한계

- self-hosted auth와 background jobs는 `v3` 확장 단계에서 다룬다.
- 화면 IA 설명이 실제 운영 KPI 설계 전체를 대신하지는 않는다.
