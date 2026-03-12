# commerce-backend

7개 랩에서 다룬 개념을 하나의 커머스 도메인으로 다시 조합해 보는 baseline capstone입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 인증, 카탈로그, 장바구니, 주문, 운영성을 한 도메인 안에서 다시 엮어야 최종 서비스 구성이 보입니다.
- 하지만 첫 통합 캡스톤은 모든 것을 깊게 구현하기보다, 이후 업그레이드의 기준선을 남기는 것이 더 중요합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- Spring modular monolith 형태로 auth, catalog, cart, order surface를 한 코드베이스에 조합했습니다.
- 상품 조회와 관리, 장바구니, 주문 흐름을 baseline 수준으로 연결했습니다.
- `commerce-backend-v2`가 왜 필요한지 설명할 수 있도록 의도적으로 얕은 부분을 남겼습니다.

## 핵심 설계 선택

- 마이크로서비스 분해보다 모듈형 모놀리스를 선택해 코드 읽기와 설명 가능성을 높였습니다.
- 랩 코드를 import하지 않고 같은 문제를 캡스톤 안에서 다시 구현했습니다.
- 이 버전은 "최종 답"이 아니라 비교용 baseline이라는 역할을 분명히 했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- persisted auth의 깊이
- payment flow와 idempotency 처리
- outbox -> Kafka -> notification의 완전한 비동기 연결

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
- 업그레이드 버전: [../commerce-backend-v2/README.md](../commerce-backend-v2/README.md)
