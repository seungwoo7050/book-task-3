# J-edge-gateway-lab

public API는 유지하면서 내부 서비스는 분리하고 싶을 때 필요한 edge gateway 랩입니다. 쿠키와 CSRF를 gateway에만 두고, 내부 서비스는 bearer token과 `X-Request-ID`만 받도록 정리하는 흐름을 다룹니다.

## 문제 요약

- 서비스가 분리된 뒤에도 외부 클라이언트는 하나의 API만 보고 싶다. 이 랩은 gateway가 public API shape를 유지하고, cookie와 CSRF를 edge에만 두며, 내부 서비스에는 request id와 bearer token만 전달하는 구조를 연습한다.
- gateway가 `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지한다.
- 로그인 후 쿠키가 gateway에서만 설정된다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- gateway public auth / platform route
- request id propagation
- 내부 서비스 fan-out

## 핵심 설계 선택

- edge gateway의 역할
- cookie + CSRF를 edge로 모으는 이유
- request id 전파
- API gateway 제품 기능 전체를 복제하지 않습니다.
- rate limiting, circuit breaker, service discovery는 문서 수준으로만 남깁니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- circuit breaker
- service discovery
- 고급 edge cache

## 다음 랩 또는 비교 대상

- 다음 단계는 [K-distributed-ops-lab](../K-distributed-ops-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
