# 지식 인덱스

## 재사용 가능한 개념

- WebSocket은 HTTP의 확장이 아니라 별도의 연결 수명주기다.
- 시간 기반 테스트는 경계값을 그대로 쓰면 흔들리기 쉽다.
- 연결 관리 구조는 disconnect 시 빈 컨테이너 정리까지 포함해야 한다.

## 용어집

- `presence`: 사용자가 현재 연결되어 있는지에 대한 단기 상태
- `fan-out`: 하나의 이벤트를 여러 활성 연결로 퍼뜨리는 전달 방식
- `TTL`: 상태를 유효하다고 보는 시간 상한

## 참고 자료

- 제목: `labs/F-realtime-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 새 문제 프레이밍에 실시간 범위와 성공 기준을 맞추기 위해 확인했다.
  - 배운 점: 이 랩은 실시간 제품 전체가 아니라 연결 모델의 핵심을 보여 주는 데 초점이 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `labs/F-realtime-lab/fastapi/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: Redis 포함 Compose 구조와 현재 워크스페이스 범위를 active 문서 기준으로 다시 확인하기 위해 읽었다.
  - 배운 점: 이 랩의 학습 가치는 Redis 자체보다 연결 모델의 분리에 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `05-development-timeline.md`에 실행 범위와 확장 경계를 더 명확히 적었다.
