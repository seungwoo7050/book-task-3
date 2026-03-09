# 01-rpc-framing 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/ddia-distributed-systems/01-rpc-framing
cd go/ddia-distributed-systems/01-rpc-framing

go mod init study.local/ddia-distributed-systems/01-rpc-framing
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/rpc-framing
mkdir -p internal/framing internal/rpc
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

이 프로젝트는 외부 의존성이 없다. Go 표준 라이브러리의 `net`, `encoding/json`, `encoding/binary`, `sync`, `sync/atomic`만 사용한다. shared 패키지도 불필요.

## Phase 1 — 문제 정의

### 1-1. problem/README.md 작성
- TCP stream에서 message boundary 복원
- 동시 요청 시 correlation id로 응답 매칭
- 출처: `legacy/distributed-cluster/rpc-network` 레거시 코드

### 1-2. docs/concepts/ 작성
- `frame-boundary.md`: TCP는 바이트 스트림, `[4-byte length][payload]` 프레이밍 설명
- `pending-map.md`: correlation id → pending call map 패턴, connection close 시 전체 정리 필요성

## Phase 2 — Framing 계층 구현

파일: `internal/framing/framing.go`

### 2-1. Encode 함수
```go
func Encode(message any) ([]byte, error)
```
- `json.Marshal` → 4바이트 big-endian length prefix 부착
- `binary.BigEndian.PutUint32`로 길이 인코딩

### 2-2. Decoder 구조체
```go
type Decoder struct {
    buffer []byte
}
```
- 상태를 가진 디코더: chunk를 내부 버퍼에 누적
- `Feed(chunk []byte) ([][]byte, error)` — 핵심 메서드

### 2-3. Feed 구현 세부
- `for len(buffer) >= 4` 루프로 가용 프레임 반복 추출
- `totalLength < 4` 검사로 overflow/잘못된 프레임 방어
- `append([]byte(nil), ...)` 패턴으로 슬라이스 메모리 공유 방지
- 프레임 부족 시 `break`하고 다음 Feed 대기

### 2-4. 설계 결정
- JSON vs Protobuf: 디버깅 편의를 위해 JSON 선택
- 4바이트 길이: 최대 ~4GB 메시지 지원, 실용적으로 충분

## Phase 3 — RPC 서버 구현

파일: `internal/rpc/rpc.go`

### 3-1. 메시지 타입 정의
```go
type request struct {
    Type          string          `json:"type"`
    CorrelationID string          `json:"correlation_id"`
    Method        string          `json:"method"`
    Params        json.RawMessage `json:"params"`
}

type response struct {
    Type          string          `json:"type"`
    CorrelationID string          `json:"correlation_id"`
    Result        json.RawMessage `json:"result,omitempty"`
    Error         string          `json:"error,omitempty"`
}
```
- `json.RawMessage`으로 params/result의 지연 역직렬화
- `omitempty`로 불필요한 필드 제거

### 3-2. Handler 타입
```go
type Handler func(context.Context, json.RawMessage) (any, error)
```

### 3-3. Server 구현
- `NewServer(addr)` → `Register(method, handler)` → `Start()`
- `net.Listen("tcp", addr)`: 포트 0을 사용하면 OS가 빈 포트 할당
- 연결마다 goroutine: `go server.handleConn(conn)`
- 연결 추적: `conns map[net.Conn]struct{}` (Close 시 전체 정리)
- `sync.Mutex`로 `conns` 맵 보호

### 3-4. handleConn 구현
- 연결마다 독립적인 `framing.Decoder` 생성
- 4096 바이트 read buffer
- 디코딩된 각 요청을 `go server.dispatch(conn, req)`로 처리

### 3-5. dispatch 구현
- 핸들러 미등록: `unknown method` 에러 응답
- 핸들러 에러: 에러 메시지를 응답으로 전송
- 정상: 결과를 JSON 직렬화하여 응답
- **모든 경로에서 응답을 보냄** — pending call 누수 방지

### 3-6. Addr() 헬퍼
- `server.listener.Addr().String()` — 클라이언트에게 실제 바인딩 주소 제공 (포트 0 사용 시 필수)

## Phase 4 — RPC 클라이언트 구현

### 4-1. Client 구조체
```go
type Client struct {
    addr    string
    conn    net.Conn
    decoder *framing.Decoder
    mu      sync.Mutex
    pending map[string]pendingCall
    nextID  uint64
    closed  chan struct{}
}
```
- `closed` 채널: 연결 종료 시그널 (select에서 사용)
- `nextID`: atomic 카운터로 correlation ID 생성

### 4-2. Connect
- `net.Dial("tcp", addr)` → 연결 수립
- `go client.readLoop()` — 백그라운드 응답 수신 루프 시작

### 4-3. Call 구현
1. `json.Marshal(params)` → 파라미터 직렬화
2. `atomic.AddUint64(&client.nextID, 1)` → correlation ID 생성
3. pending map에 `pendingCall{response: make(chan response, 1)}` 등록
4. 요청 프레임 인코딩 및 전송
5. `select` 대기:
   - `call.response` → 정상 응답
   - `ctx.Done()` → 타임아웃
   - `client.closed` → 연결 종료

### 4-4. readLoop 구현
- 무한 루프로 서버 응답 수신
- `framing.Decoder.Feed`로 프레임 디코딩
- `correlation_id`로 pending call 조회 → 채널에 응답 전송 → map에서 제거
- 에러 발생 시 `failAll` 호출 + `closed` 채널 닫기

### 4-5. failAll / failPending
- `failAll`: 모든 pending call에 에러 전파 → 메모리 누수/무한 대기 방지
- `failPending`: 특정 하나의 pending call 정리

### 4-6. Close
- 연결 닫기 + `failAll` + `closed` 채널 닫기

## Phase 5 — 테스트 작성

파일: `tests/rpc_test.go`

```bash
GOWORK=off go test -v ./tests/
```

| 테스트 | 검증 내용 |
|--------|----------|
| TestDecoderHandlesSingleMessage | Encode → Feed → 1개 payload 반환 |
| TestDecoderHandlesSplitChunks | 프레임을 반으로 쪼개서 Feed → 두 번째에 메시지 완성 |
| TestRPCServerClientRoundTrip | echo 핸들러 왕복 테스트 |
| TestRPCHandlesConcurrentCalls | 3개 goroutine에서 동시 Call, 각각 올바른 결과 |
| TestRPCPropagatesServerErrorsAndTimeout | 서버 에러 전파 + 20ms 타임아웃 |

## Phase 6 — 데모 CLI

파일: `cmd/rpc-framing/main.go`

```bash
cd cmd/rpc-framing
go run .
```

예상 출력:
```
pong:hello
```

시나리오: ping 핸들러 등록 → 서버 시작 → 클라이언트 연결 → Call("ping") → 응답 출력

## Phase 7 — 검증 및 마무리

```bash
GOWORK=off go test -v ./tests/
gofmt -w internal/ cmd/ tests/
go vet ./...
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 2개 (framing.go, rpc.go) |
| framing.go | ~45줄 |
| rpc.go | ~250줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 5개 |
| 외부 의존성 | 없음 (Go 표준 라이브러리만) |

## 핵심 패턴

- **Length-prefix framing**: 모든 후속 프로젝트의 네트워크 통신 기반
- **Correlation ID + Pending Map**: 동시 RPC의 표준 패턴
- **failAll on disconnect**: pending call 누수 방지의 필수 패턴
- **포트 0**: 테스트 시 OS 포트 할당으로 포트 충돌 회피
