# 12 gRPC Microservices Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - ProductStore로 CRUD 바닥을 먼저 세운다

- 목표: ProductStore로 CRUD 바닥을 먼저 세운다
- 변경 단위: `solution/go/server/store/store.go`의 `NewProductStore`
- 핵심 가설: `NewProductStore`로 CRUD 바닥을 먼저 세우면 transport와 proto는 뒤에서 갈아끼우기 쉽다고 봤다.
- 반드시 넣을 코드 앵커: `NewProductStore`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestCreateAndGet`였다.
- 새로 배운 것 섹션 포인트: proto-first는 API 계약을 코드보다 먼저 고정하는 접근이다.
- 다음 섹션 연결 문장: server, client, interceptor로 transport 경계를 얹는다
### 2. Phase 2 - server, client, interceptor로 transport 경계를 얹는다

- 목표: server, client, interceptor로 transport 경계를 얹는다
- 변경 단위: `solution/go/server/interceptors/interceptors.go`의 `LoggingUnaryInterceptor`
- 핵심 가설: `LoggingUnaryInterceptor`에 공통 interceptor를 모아 두면 client, server 양쪽 계약을 더 선명하게 드러낼 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `LoggingUnaryInterceptor`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]`였다.
- 새로 배운 것 섹션 포인트: round-robin과 retry는 감각을 보여 주지만, production-grade observability나 timeout 정책은 더 필요하다.
- 다음 섹션 연결 문장: store tests와 race 검증으로 rpc 표면을 잠근다
### 3. Phase 3 - store tests와 race 검증으로 rpc 표면을 잠근다

- 목표: store tests와 race 검증으로 rpc 표면을 잠근다
- 변경 단위: `solution/go/server/store/store_test.go`의 `TestCreateAndGet`
- 핵심 가설: `TestCreateAndGet`와 race 테스트가 있어야 store와 rpc 표면이 같이 검증된다고 봤다.
- 반드시 넣을 코드 앵커: `TestCreateAndGet`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]`였다.
- 새로 배운 것 섹션 포인트: unary call만 보고 gRPC를 “HTTP와 크게 다르지 않다”고 오해하기 쉽다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices && cd solution/go && go test -run TestCreateAndGet -v ./server/store)
```

```text
=== RUN   TestCreateAndGet
--- PASS: TestCreateAndGet (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/store	(cached)
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/02-distributed-systems/12-grpc-microservices && cd solution/go && go test -v -race -count=1 ./...)
```

```text
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/client/cmd	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/cmd	[no test files]
?   	github.com/woopinbell/go-backend/study/02-distributed-systems/12-grpc-microservices/server/interceptors	[no test files]
=== RUN   TestCreateAndGet
--- PASS: TestCreateAndGet (0.00s)
=== RUN   TestGetNotFound
--- PASS: TestGetNotFound (0.00s)
=== RUN   TestUpdate
--- PASS: TestUpdate (0.00s)
=== RUN   TestDelete
--- PASS: TestDelete (0.00s)
=== RUN   TestList
=== RUN   TestList/no_filter
=== RUN   TestList/filter_electronics
=== RUN   TestList/filter_books
=== RUN   TestList/filter_nonexistent
--- PASS: TestList (0.00s)
    --- PASS: TestList/no_filter (0.00s)
    --- PASS: TestList/filter_electronics (0.00s)
    --- PASS: TestList/filter_books (0.00s)
    --- PASS: TestList/filter_nonexistent (0.00s)
... (2 more lines)
```
