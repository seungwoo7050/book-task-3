# commerce-backend-v2

이 레포의 대표 결과물로, baseline capstone을 같은 도메인에서 더 깊게 구현한 portfolio-grade Spring 백엔드입니다.

- 상태: `verified portfolio capstone`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 한국 주니어 Spring 백엔드 채용 공고에서 반복되는 요구사항을 한 서비스 안에서 설명 가능한 수준으로 연결해야 합니다.
- baseline capstone이 남긴 얕은 부분을 보강하되, 도메인을 바꾸지 않고 같은 커머스 문제를 더 깊게 풀어야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- persisted auth, JPA + Flyway domain modeling, Redis cart/throttling, idempotent payment, outbox + Kafka notification을 한 modular monolith에 연결했습니다.
- auth, catalog, cart, order, payment, notification, global 패키지로 경계를 나눴습니다.
- baseline과 비교해 "무엇을 더 구현했고 무엇은 아직 남겼는가"를 README와 docs에서 바로 설명할 수 있게 했습니다.

## 핵심 설계 선택

- 도메인은 유지하고 구현 깊이만 올려 baseline 대비 개선점을 명확히 했습니다.
- microservices보다 modular monolith를 유지해 코드 탐색과 인터뷰 설명 난도를 낮췄습니다.
- Redis와 Kafka는 키워드 장식이 아니라 cart, throttling, outbox handoff라는 구체적 문제에만 연결했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

`make test`에는 Testcontainers 기반 messaging test가 포함됩니다. 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- 실제 Google OAuth console integration
- production payment provider integration
- live AWS provisioning과 장기 Kafka 운영 검증

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 아키텍처와 검증 메모: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
- baseline capstone: [../commerce-backend/README.md](../commerce-backend/README.md)
