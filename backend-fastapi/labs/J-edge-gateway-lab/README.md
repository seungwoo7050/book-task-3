# J-edge-gateway-lab

public API는 유지하면서 내부 서비스는 분리하고 싶을 때 필요한 edge gateway 랩입니다. 쿠키와 CSRF를 gateway에만 두고, 내부 서비스는 bearer token과 `X-Request-ID`만 받도록 정리하는 흐름을 다룹니다.

## 이 랩에서 배우는 것

- edge gateway의 역할
- cookie + CSRF를 edge로 모으는 이유
- request id 전파
- public route shape 유지와 내부 fan-out

## 선수 지식

- [H-service-boundary-lab](../H-service-boundary-lab/README.md)
- 브라우저 쿠키와 bearer token 차이

## 구현 범위

- gateway public auth / platform route
- request id propagation
- 내부 서비스 fan-out

## 일부러 단순화한 점

- API gateway 제품 기능 전체를 복제하지 않습니다.
- rate limiting, circuit breaker, service discovery는 문서 수준으로만 남깁니다.

## 실행 방법

1. [problem/README.md](problem/README.md)를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 gateway 중심 스택을 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 edge 설계를 복습합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. public route와 internal route를 나눠 적습니다.
2. 쿠키가 왜 gateway에만 있어야 하는지 확인합니다.
3. `X-Request-ID`가 내부 서비스까지 가는지 확인합니다.

## 포트폴리오로 확장하려면

- BFF, gateway auth policy, edge cache를 실험할 수 있습니다.
- 실패 전파 정책과 fallback 기준을 README에 별도로 적어 두면 좋습니다.
