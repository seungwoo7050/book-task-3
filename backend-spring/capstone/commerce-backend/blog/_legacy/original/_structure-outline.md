# commerce-backend Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리할 초안이 없다.
- 시리즈 방향:
  - baseline capstone이 어떤 통합 지점을 만들고 어떤 깊이를 일부러 남겼는지 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널 기준으로 `make test`, `make smoke`, Compose 검증 기록을 사용한다.
- 파일 계획:
  - `00-series-map.md`: baseline이 왜 필요한지 설명한다.
  - `10-assembling-the-baseline.md`: scope 고정 -> service 조합 -> end-to-end flow를 다룬다.
  - `20-checkout-proof-and-remaining-gaps.md`: checkout 증명과 deliberately shallow한 영역을 정리한다.
- 반드시 강조할 것:
  - baseline의 역할은 완성품이 아니라 비교 기준점이다.
  - contract-level auth와 shallow checkout은 약점이 아니라 의도적 설계 선택이다.
