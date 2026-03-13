# 05 HTTP REST Basics 시리즈 맵

이 시리즈는 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 썼다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다.

## 이번 재작성 범위

- 문제 계약: [`README.md`](../../01-backend-core/05-http-rest-basics/README.md), [`problem/README.md`](../../01-backend-core/05-http-rest-basics/problem/README.md)
- 구현 표면:
- `solution/go/internal/api/api.go`
- `solution/go/internal/api/api_test.go`
- `solution/go/cmd/server/main.go`
- 검증 표면: `cd solution/go && go test -v ./internal/api`, `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
- 개념 축: GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다., 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다., validation 실패는 `422`로, 잘못된 JSON이나 path parameter는 `400`으로 다루는 편이 읽기 쉽다.

## 챕터 구성

1. [`01-evidence-ledger.md`](01-evidence-ledger.md)
   실제 코드, 테스트, CLI, git history에서 복원한 chronology ledger
2. [`_structure-outline.md`](_structure-outline.md)
   최종 blog를 어떤 순서와 코드 앵커로 전개할지 먼저 고정한 구조 설계
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md)
   구현 순서, 판단 전환점, 검증 신호를 한 편으로 다시 쓴 최종 blog

## 이번에 따라간 질문

가장 작은 task API에서 route, validation, idempotency를 한 서버로 엮는다.
