# 17 Game Store Capstone Structure

## 이 글이 답할 질문

- 문제 정의와 답안 요약, docs/notion을 분리해 제출 가능한 공개 표면을 정리한다.
- OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `04-capstone/17-game-store-capstone` 안에서 `30-relay-http-and-ops-surface.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 9단계: httpapi 구현 -> 10단계: relay 구현 -> 11단계: cmd/api 진입점
- 세션 본문: `solution/go/internal/httpapi/handler.go, solution/go/internal/relay/relay.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/httpapi/handler.go`
- 코드 앵커 2: `solution/go/internal/relay/relay.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.
- 마지막 단락: 다음 글에서는 `40-repro-and-e2e-hardening.md`에서 이어지는 경계를 다룬다.
