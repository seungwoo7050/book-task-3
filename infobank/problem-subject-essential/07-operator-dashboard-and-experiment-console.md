# 07-operator-dashboard-and-experiment-console 문제지

## 왜 중요한가

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 정리해 추천 시스템의 운영 면을 보여 주는 단계다.

## 목표

시작 위치의 구현을 완성해 추천 시스템이 단일 API가 아니라 운영 도구까지 포함한다는 점을 보여 준다, 학생이 자기 포트폴리오에서 운영자 UI를 어떻게 설명할지 참고할 수 있다, 최종 capstone의 화면 중심 시연 경로가 명확해진다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/package.json`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 추천 시스템이 단일 API가 아니라 운영 도구까지 포함한다는 점을 보여 준다.
- 학생이 자기 포트폴리오에서 운영자 UI를 어떻게 설명할지 참고할 수 있다.
- 최종 capstone의 화면 중심 시연 경로가 명확해진다.

## 제외 범위

- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `apiBaseUrl`와 `apiFetch`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `runs candidate recommendation and release gate flow`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react && npm run test`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react && npm run test
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`07-operator-dashboard-and-experiment-console_answer.md`](07-operator-dashboard-and-experiment-console_answer.md)에서 확인한다.
