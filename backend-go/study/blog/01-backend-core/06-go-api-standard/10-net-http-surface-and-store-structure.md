# 06 Go API Standard Structure

## 이 글이 답할 질문

- 표준 라이브러리만으로 RESTful JSON API를 설계해야 한다.
- 외부 프레임워크를 빼고 표준 라이브러리만 사용해 HTTP 기초를 드러냈다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/06-go-api-standard` 안에서 `10-net-http-surface-and-store.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대와 구조 결정 -> Phase 2: 데이터 레이어 구현
- 세션 본문: `cmd/api/, internal/data/models.go, internal/data/movies.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/data/movies.go`
- 코드 앵커 2: `solution/go/cmd/api/main.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.
- 마지막 단락: 다음 글에서는 `20-middleware-shutdown-and-proof.md`에서 이어지는 경계를 다룬다.
