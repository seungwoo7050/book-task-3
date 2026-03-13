# commerce-backend-v2 Structure Outline

- 기존 blog 처리:
  - 기존 `blog/`가 없어서 격리 대상이 없다.
- 시리즈 방향:
  - baseline 대비 어디서 깊어졌는지를 auth, checkout, payment/outbox proof 세 축으로 복원한다.
- 작업 환경 반영:
  - macOS + VSCode 통합 터미널에서 `make test`, `make smoke`, Compose 검증을 근거로 쓴다.
  - IntelliJ run configuration이나 IDE 데이터베이스 브라우저 대신 코드와 CLI를 중심에 둔다.
- 파일 계획:
  - `00-series-map.md`: 대표 capstone의 문제와 근거를 정리한다.
  - `10-from-auth-to-checkout-foundation.md`: modular monolith 선택, persisted auth, cart/checkout foundation을 다룬다.
  - `20-closing-payment-outbox-and-proof.md`: payment idempotency, outbox/Kafka, Testcontainers proof를 다룬다.
- 반드시 강조할 것:
  - 같은 도메인에서 깊이만 올렸기 때문에 baseline 대비 설명력이 생긴다.
  - Redis와 Kafka는 정당화된 지점에만 붙어 있다.
