# 07 운영자 대시보드와 실험 콘솔

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 정리해 추천 시스템의 운영 면을 보여 주는 단계다.

## 이 단계에서 배우는 것

- 운영자 화면에서 무엇을 먼저 보여 줘야 하는지
- catalog 관리, 실험 관리, release candidate 관리를 한 콘솔로 묶는 법
- 실험 결과와 운영 작업을 같은 정보 구조에서 다루는 방식

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `08-capstone-submission/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `08-capstone-submission/v2-submission-polish/tests/e2e/recommendation.spec.ts`

## 현재 상태

- 운영 콘솔은 `v1`에서 시작해 `v2`에서 제출용 시연 화면으로 정리된다.
- 이 stage는 추천 품질 실험과 운영 작업을 한 화면 구조로 묶는 이유를 설명한다.

## 포트폴리오로 가져갈 것

- 운영자 대시보드 IA 설계
- 실험 콘솔과 release console을 같은 제품 서사로 묶는 방식
