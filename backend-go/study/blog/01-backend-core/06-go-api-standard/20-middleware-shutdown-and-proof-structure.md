# 06 Go API Standard Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- DB를 의도적으로 제외해 handler/model/middleware 구조와 종료 시퀀스에 집중하게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/06-go-api-standard` 안에서 `20-middleware-shutdown-and-proof.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 3: 핸들러와 미들웨어 구현 -> Phase 4: 서버 기동과 graceful shutdown -> Phase 5: 테스트 -> Phase 6: problem 디렉터리와 Makefile
- 세션 본문: `internal/data/movies_test.go, cmd/api/handlers_test.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/cmd/api/middleware.go`
- 코드 앵커 2: `solution/go/cmd/api/handlers_test.go`
- 코드 설명 초점: 이 블록은 요청 수명주기를 감싸는 순서를 고정한다. recovery, logging, auth, CORS는 순서가 틀리면 의미가 달라지기 때문에 이 코드가 글의 축이 된다.
- 개념 설명: JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다.
- 마지막 단락: `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.
