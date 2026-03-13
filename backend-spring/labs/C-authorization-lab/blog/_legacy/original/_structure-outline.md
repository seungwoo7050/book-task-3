# C-authorization-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리할 초안이 없다.
- 시리즈 방향:
  - 인증과 분리된 authorization 문제를 membership lifecycle 중심으로 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널에서 `make`와 MockMvc 테스트를 돌린 기록으로 쓴다.
  - IntelliJ security annotation 설정 화면 같은 IDE 중심 설명은 넣지 않는다.
- 파일 계획:
  - `00-series-map.md`: authorization 랩이 auth 랩과 왜 분리돼야 하는지 설명한다.
  - `10-development-timeline.md`: scope 고정 -> membership lifecycle 구현 -> MockMvc 검증 순서를 따른다.
- 반드시 강조할 것:
  - `invite -> accept -> role change`는 authorization을 설명하는 최소 sequence다.
  - method security보다 service logic의 명시성이 먼저다.
