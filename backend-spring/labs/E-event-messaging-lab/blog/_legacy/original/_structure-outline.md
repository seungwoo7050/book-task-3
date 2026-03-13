# E-event-messaging-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리 대상이 없다.
- 시리즈 방향:
  - outbox를 "Kafka 입문"이 아니라 "이벤트 경계 복원" 관점으로 쓴다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널에서 `make test`와 `docker compose`를 직접 호출하는 흐름을 근거로 남긴다.
- 파일 계획:
  - `00-series-map.md`: outbox가 왜 현재 단계의 중심인지 설명한다.
  - `10-development-timeline.md`: scope 고정 -> pending row 설계 -> publish lifecycle 검증으로 전개한다.
- 반드시 강조할 것:
  - emit과 publish는 다른 문제다.
  - `PENDING`과 `PUBLISHED`라는 상태 이름 자체가 설계 판단의 결과다.
