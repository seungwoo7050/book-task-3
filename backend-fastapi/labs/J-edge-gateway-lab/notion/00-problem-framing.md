# 문제 프레이밍

## 학습 목표

J 랩의 중심은 “public API는 그대로인데 내부는 분리되었다”는 상태를 만드는 것이다. gateway는 브라우저와 만나는 서비스이고, 내부 서비스는 bearer claims와 request id만 받도록 제한한다.

## 왜 중요한가

- 서비스가 여러 개로 나뉘어도 외부 클라이언트는 기존 route shape를 잃지 않는 편이 현실적이다.
- 브라우저 쿠키, CSRF, refresh token 같은 상태를 내부 서비스까지 퍼뜨리면 edge 책임이 흐려진다.
- gateway는 단순 프록시라기보다 “public contract를 보존하는 경계”라는 점을 이해해야 한다.

## 선수 지식

- H 랩의 claim 기반 service boundary
- I 랩의 event handoff와 eventual consistency
- cookie, CSRF, bearer token의 차이에 대한 기본 감각

## 성공 기준

- 외부 클라이언트는 `/api/v1/auth/*`, `/api/v1/platform/*`만 보면 된다.
- gateway가 쿠키/CSRF를 처리하고 내부 서비스에는 bearer claims만 전달해야 한다.
- `X-Request-ID`가 gateway에서 생성되어 내부 호출에 그대로 전파되어야 한다.
- 내부 서비스 장애는 gateway에서 503 등 upstream 오류로 표면화되어야 한다.

## 일부러 제외한 범위

- API gateway product나 service mesh
- global rate limiting과 복잡한 edge cache
- full OAuth proxy 구성

## 이 랩이 답하려는 질문

- 왜 edge 책임은 내부 도메인 책임과 다른가
- public API를 유지한 채 내부 서비스를 바꾸려면 어느 경계를 먼저 고정해야 하는가
- gateway가 생기면 테스트와 장애 표면화는 어떻게 달라지는가
