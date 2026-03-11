# Script Notes

현재 이 프로젝트는 별도의 채점 스크립트보다 `go test`와 demo 실행을 공식 검증 경로로 사용합니다.

- `GOWORK=off go test ./...`: 자료구조 계약 검증
- `GOWORK=off go run ./cmd/skiplist-demo`: 정렬 순회와 tombstone 상태를 눈으로 확인
