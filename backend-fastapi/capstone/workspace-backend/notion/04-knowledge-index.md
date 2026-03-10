# 지식 인덱스

## 재사용 가능한 개념

- 작은 랩의 코드를 그대로 합치는 것과, 개념을 통합 설계로 다시 구현하는 것은 다르다.
- 통합 프로젝트에서는 기능 버그보다 경계와 순서 문제를 먼저 점검해야 한다.
- cookie + CSRF, queue + realtime, RBAC + 협업 데이터처럼 교차 지점이 많은 곳이 설명 가치도 가장 크다.

## 용어집

- `integration boundary`: 두 개 이상의 하위 주제가 만나는 경계
- `bootstrap`: 앱 시작 시 필요한 초기 설정이나 스키마 준비 단계
- `capstone`: 여러 학습 단위를 하나의 완성형 프로젝트로 다시 묶는 마지막 프로젝트

## 참고 자료

- 제목: `capstone/workspace-backend/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: capstone의 통합 범위와 제외 범위를 새 노트에 맞추기 위해 확인했다.
  - 배운 점: 이 프로젝트의 핵심은 기능 수가 아니라 여러 경계를 한 구조 안에서 설명하는 데 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `capstone/workspace-backend/fastapi/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 현재 capstone 실행 범위와 Compose 구성을 active 문서 기준으로 다시 확인하기 위해 읽었다.
  - 배운 점: capstone은 랩의 합이 아니라, 통합 경계를 스스로 다시 설명해야 설득력이 생긴다.
  - 반영 결과: 새 `00-problem-framing.md`, `01-approach-log.md`, `05-development-timeline.md`에 반영했다.
