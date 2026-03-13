# A-auth-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/` 초안이 없어서 격리 대상은 없다.
- 시리즈 방향:
  - 로컬 계정 인증의 최소 lifecycle을 먼저 고정하고, refresh rotation과 CSRF 경계를 코드와 테스트로 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널 기준으로 쓴다.
  - IntelliJ 실행 화면 대신 `make`, `./gradlew`, MockMvc 검증을 중심 근거로 둔다.
- 파일 계획:
  - `00-series-map.md`: 프로젝트 범위, 근거, 읽는 순서를 짧게 잡는다.
  - `10-development-timeline.md`: scope 고정 -> in-memory auth 구현 -> MockMvc/CLI 검증 순서를 따라간다.
- 반드시 강조할 것:
  - refresh rotation은 이전 refresh token 폐기까지 포함한 상태 전이다.
  - cookie를 아직 완전히 붙이지 않아도 CSRF 경계를 API 레벨에서 설명할 수 있다.
