# 14 Cockroach TX Structure

## 이 글이 답할 질문

- balance version conflict와 idempotency cached response를 서비스 경계에서 구분한다.
- HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/14-cockroach-tx` 안에서 `20-purchase-service-and-http-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 7단계: Service 구현 -> 8단계: HTTP Handler -> 9단계: cmd/server 진입점
- 세션 본문: `solution/go/service/purchase.go, solution/go/handler/purchase.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/service/purchase.go`
- 코드 앵커 2: `solution/go/handler/purchase.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: optimistic locking은 `version` 컬럼으로 충돌을 감지한다.
- 마지막 단락: 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.
