# D-data-jpa-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리 대상이 없다.
- 시리즈 방향:
  - CRUD를 만들었다는 요약이 아니라 JPA 경계와 optimistic locking을 어떤 순서로 노출했는지 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널 기준으로 `make test`, `make smoke` 흐름을 근거로 쓴다.
- 파일 계획:
  - `00-series-map.md`: JPA 랩의 문제와 근거를 짧게 잡는다.
  - `10-development-timeline.md`: scope 고정 -> entity/service 설계 -> version conflict 검증 순서를 쓴다.
- 반드시 강조할 것:
  - `@Version`은 동시성 제어를 API 계약으로 끌어오는 장치다.
  - page listing과 conflict 테스트가 함께 있어야 "설계 선택"이 보인다.
