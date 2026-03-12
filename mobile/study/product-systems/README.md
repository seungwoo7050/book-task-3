# product-systems

`product-systems`는 단일 화면 구현을 넘어 local-first 제품 흐름과 release rehearsal을 다루는 단계다.
문제는 UI보다 데이터 흐름, 재시도 규칙, 배포 재현성으로 이동한다.

## 포함 프로젝트

1. [01-offline-sync-foundations](01-offline-sync-foundations/README.md)
2. [02-realtime-chat](02-realtime-chat/README.md)
3. [03-app-distribution](03-app-distribution/README.md)

## 왜 이 순서인가

- `01-offline-sync-foundations`에서 queue/retry/idempotency를 독립적으로 익힌다.
- `02-realtime-chat`에서 그 규칙을 local-first 채팅 모델로 통합한다.
- `03-app-distribution`에서 제품 동작과 배포 리허설을 분리해 release discipline을 다룬다.

## 다음 단계

제품형 문제를 다룬 뒤 [capstone](../capstone/README.md)에서 system contract와 hiring-facing 완성작을 분리해 마무리한다.
