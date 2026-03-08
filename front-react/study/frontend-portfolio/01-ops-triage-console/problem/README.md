# Product Brief

프로비넌스: `authored`

## 제품 정의

`Ops Triage Console`은 여러 채널에서 들어오는 이슈를 한 명의 운영자가 빠르게 정리하고 우선순위를 지정하며 적절한 팀으로 라우팅하는 콘솔이다.

## 핵심 사용자

- support escalation을 정리하는 운영자
- QA 결과를 triage하는 운영자
- customer feedback와 monitoring alert를 함께 보는 운영자

## 핵심 작업

1. queue 상태를 빠르게 파악한다
2. 문제가 큰 이슈를 먼저 찾는다
3. 상태, 우선순위, 라벨, route team을 변경한다
4. 여러 건을 한 번에 정리한다
5. 실패 시 retry하고, 잘못된 변경은 undo한다

## 포함 범위

- dashboard summary
- searchable triage queue
- faceted filters
- saved views
- bulk actions
- issue detail panel
- operator note
- demo reset
- chaos/failure simulation

## 제외 범위

- 실제 인증
- 실제 DB
- 멀티유저 실시간 협업
- 실제 백엔드 API

## 품질 기준

- data-heavy UI라도 읽기 쉬워야 한다
- keyboard-only 주요 흐름이 가능해야 한다
- loading, empty, error, retry 상태가 모두 있어야 한다
- unit, integration, E2E 검증을 갖춰야 한다

