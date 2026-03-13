# 13 Distributed Log Core Evidence Ledger

## 30 tests-and-bench-evidence

- 시간 표지: 7단계: 전체 테스트 및 검증 -> 8단계: go.work 등록
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/log/log_test.go`, `solution/go/log/segment_test.go`
- 처음 가설: 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 실제 조치: 

CLI:

```bash
# 전체 테스트 실행
cd 13-distributed-log-core/go
go test ./... -v

# 커버리지 측정
go test ./log/ -coverprofile=coverage.out
go tool cover -html=coverage.out

# Race condition 검사
go test ./log/ -race -v

# study/go.work에 모듈 추가
cd ../../
# go.work에 use ./02-distributed-systems/13-distributed-log-core/go 추가
```

- 검증 신호:
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: replication layer는 study 본선 범위에서 제외했다.
- 핵심 코드 앵커: `solution/go/log/log_test.go`
- 새로 배운 것: segment는 store와 index를 묶은 관리 단위다.
- 다음: replication layer는 study 본선 범위에서 제외했다.
