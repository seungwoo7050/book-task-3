# 13 Distributed Log Core Evidence Ledger

## 20 log-abstraction-and-rotation

- 시간 표지: 5단계: Log 구현 (다중 Segment 관리) -> 6단계: 에러 정의
- 당시 목표: mmap index와 segment rotation을 테스트 및 benchmark와 함께 정리했다.
- 변경 단위: `log/log.go`, `log/errors.go`
- 처음 가설: 파일 포맷과 segment lifecycle을 먼저 구현해 분산 복제 이전의 로컬 불변식을 학습하게 했다.
- 실제 조치: `log/log.go` 작성. 주요 결정: `setup()`: 디렉토리 스캔 → `.store` 파일 파싱 → baseOffset 정렬 → Segment 복원 `Append()`: activeSegment.IsFull()이면 newSegment() 호출 `Read()`: `sort.Search`로 이진 탐색 → 올바른 Segment 찾기 `Truncate(lowest)`: lowest 미만의 Segment 모두 삭제 `Reset()`: `os.RemoveAll` → 새 Segment로 재시작 `log/errors.go` — 5개 sentinel error 정의.

CLI:

```bash
# Log 전체 테스트
go test ./log/ -run TestLog -v
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/log/log.go`
- 새로 배운 것: index는 logical offset을 물리 위치로 빠르게 찾기 위한 보조 구조다.
- 다음: 다음 글에서는 `30-tests-and-bench-evidence.md`에서 이어지는 경계를 다룬다.
