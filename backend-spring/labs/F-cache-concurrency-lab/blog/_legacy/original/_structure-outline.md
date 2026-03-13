# F-cache-concurrency-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리할 초안이 없다.
- 시리즈 방향:
  - inventory 시나리오 하나로 cache, idempotency, concurrency의 서로 다른 역할을 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널에서 `make test`, `make smoke`, Compose 검증을 근거로 쓴다.
- 파일 계획:
  - `00-series-map.md`: 왜 세 문제를 한 시나리오에 묶는지 설명한다.
  - `10-development-timeline.md`: scope 고정 -> write/read path 규칙 구현 -> MockMvc 검증으로 전개한다.
- 반드시 강조할 것:
  - idempotency key와 `synchronized`는 역할이 다르다.
  - `@Cacheable`은 read path에만 개입한다.
