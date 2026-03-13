# B-federation-security-lab Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어서 `isolate-and-rewrite` 시 격리 대상이 없다.
- 시리즈 방향:
  - federation, 2FA, audit를 "인증 강화"라는 하나의 묶음으로 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널 기준 명령과 MockMvc 검증을 중심으로 쓴다.
  - IntelliJ provider 설정 화면을 전제로 설명하지 않는다.
- 파일 계획:
  - `00-series-map.md`: 왜 이 랩이 A-auth-lab 다음 단계인지 잡는다.
  - `10-development-timeline.md`: scope 고정 -> contract-level 구현 -> MockMvc/CLI 검증으로 전개한다.
- 반드시 강조할 것:
  - state/nonce는 provider 연동 전에 먼저 설명해야 하는 값이다.
  - TOTP setup, recovery code, audit event는 모두 인증 강화의 같은 표면이다.
