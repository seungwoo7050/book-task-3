# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### key별 version chain을 저장한다
- 관련 파일: `../internal/mvcc/mvcc.go`
- 판단: `VersionStore`가 key마다 여러 version을 유지하게 해 최신 값 하나만 보는 단일-store 모델에서 벗어났습니다.

### transaction 시작 시 snapshot을 고정한다
- 관련 파일: `../internal/mvcc/mvcc.go`
- 판단: `Begin` 시점의 committed watermark를 snapshot 기준으로 삼아, 이후 들어온 commit이 바로 보이지 않게 했습니다.

### commit에서 충돌을 늦게 검증한다
- 관련 파일: `../internal/mvcc/mvcc.go`
- 판단: write 시점에는 version을 쌓고, commit 시점에 같은 key의 더 새로운 committed write가 있는지 검사하는 first-committer-wins 방식을 택했습니다.

## 검증 명령
```bash
cd go/database-internals/projects/09-mvcc
go test ./...
go run ./cmd/mvcc
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- `t2 sees x=...` 같은 데모는 snapshot isolation을 매우 짧게 설명하는 좋은 장면입니다.
- `VersionStore`와 `TransactionManager`를 분리한 구조는 저장과 정책을 어떻게 나눴는지 보여 줍니다.
- read-your-own-write와 first-committer-wins를 같은 프로젝트에서 보여 준 점도 좋은 정리 포인트입니다.
