# 05-usage-logs-metrics-and-feedback-loop 문제지

## 왜 중요한가

usage event, feedback record, experiment metadata를 DB와 API로 연결해 추천 품질 개선의 운영 루프를 설명하는 단계다.

## 목표

시작 위치의 구현을 완성해 추천 품질 개선이 일회성 실험이 아니라 운영 루프로 설명된다, 학생이 자기 프로젝트에서 어떤 운영 지표를 남겨야 할지 감을 잡는다, 후속 release gate와 operator console 단계로 자연스럽게 이어진다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/db/schema.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/manifest-validation.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/recommendation-service.test.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/package.json`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 추천 품질 개선이 일회성 실험이 아니라 운영 루프로 설명된다.
- 학생이 자기 프로젝트에서 어떤 운영 지표를 남겨야 할지 감을 잡는다.
- 후속 release gate와 operator console 단계로 자연스럽게 이어진다.

## 제외 범위

- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `buildApp`와 `catalogEntries`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `manifest validation`와 `rejects incomplete manifests`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/rerank-service.test.ts`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node && npm test -- tests/manifest-validation.test.ts tests/recommendation-service.test.ts tests/rerank-service.test.ts
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react && npm run test
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`05-usage-logs-metrics-and-feedback-loop_answer.md`](05-usage-logs-metrics-and-feedback-loop_answer.md)에서 확인한다.
