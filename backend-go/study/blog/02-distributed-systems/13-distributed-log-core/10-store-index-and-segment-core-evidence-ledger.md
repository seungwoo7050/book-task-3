# 13 Distributed Log Core Evidence Ledger

## 10 store-index-and-segment-core

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: Store 구현 (append-only 파일) -> 3단계: Index 구현 (mmap 기반) -> 4단계: Segment 구현 (Store + Index 조합)
- 당시 목표: length-prefixed store와 fixed-width index를 직접 구현해야 한다.
- 변경 단위: `log/store.go`, `log/index.go`, `log/segment.go`
- 처음 가설: Kafka형 시스템을 한 번에 복제하지 않고 append-only log 핵심 구조만 분리했다.
- 실제 조치: Go 1.22 사용, 외부 의존성 없이 표준 라이브러리만으로 구현. `log/store.go` 작성. 주요 결정: `bufio.NewWriter`로 쓰기 버퍼링 (시스템 콜 최소화) 길이 접두사: `binary.BigEndian.PutUint64` (8바이트 고정) `sync.Mutex`로 동시 접근 보호 `Read`에서 항상 `buf.Flush()` 먼저 `log/index.go` 작성.

CLI:

```bash
mkdir -p 13-distributed-log-core/solution/go/log
cd 13-distributed-log-core/go
go mod init distributed-log-core

# 파일 생성 후 첫 컴파일 확인
go build ./...
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/log/store.go`
- 새로 배운 것: store는 레코드 바이트를 순차 append하는 역할이다.
- 다음: 다음 글에서는 `20-log-abstraction-and-rotation.md`에서 이어지는 경계를 다룬다.
