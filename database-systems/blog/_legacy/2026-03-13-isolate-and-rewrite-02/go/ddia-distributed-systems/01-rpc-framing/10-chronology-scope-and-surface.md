# 10 01 RPC Framing의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `01 RPC Framing`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/README.md`, `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/tests/rpc_test.go`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find internal tests cmd -type f | sort`로 구조를 펼친 뒤 `rg -n "^func Test" tests`로 테스트 이름을 나열했다. `TestRPCPropagatesServerErrorsAndTimeout`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Encode` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find internal tests cmd -type f | sort
cmd/rpc-framing/main.go
internal/framing/framing.go
internal/rpc/rpc.go
tests/rpc_test.go
```

```bash
$ rg -n "^func Test" tests
tests/rpc_test.go:15:func TestDecoderHandlesSingleMessage(t *testing.T) {
tests/rpc_test.go:30:func TestDecoderHandlesSplitChunks(t *testing.T) {
tests/rpc_test.go:46:func TestRPCServerClientRoundTrip(t *testing.T) {
tests/rpc_test.go:75:func TestRPCHandlesConcurrentCalls(t *testing.T) {
tests/rpc_test.go:119:func TestRPCPropagatesServerErrorsAndTimeout(t *testing.T) {
```

검증 신호:

- `TestDecoderHandlesSingleMessage`는 가장 기본 표면을 보여 줬고, `TestRPCPropagatesServerErrorsAndTimeout`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Encode` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```go
func TestRPCPropagatesServerErrorsAndTimeout(t *testing.T) {
	server := rpc.NewServer("127.0.0.1:0")
	server.Register("fail", func(_ context.Context, _ json.RawMessage) (any, error) {
		return nil, errors.New("intentional failure")
	})
	server.Register("slow", func(_ context.Context, _ json.RawMessage) (any, error) {
		time.Sleep(200 * time.Millisecond)
		return map[string]string{"status": "done"}, nil
	})
	if err := server.Start(); err != nil {
		t.Fatal(err)
	}
	defer server.Close()
```

왜 이 코드가 중요했는가:

`TestRPCPropagatesServerErrorsAndTimeout`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Frame Boundary Recovery`에서 정리한 요점처럼, TCP는 message 단위가 아니라 byte stream이다. 따라서 sender가 한 번 `Write` 했다고 receiver가 한 번 `Read`로 같은 단위를 받는다는 보장이 없다.

다음:

- `Encode`와 `Decoder`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc/rpc.go`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/rpc/rpc.go`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

CLI:

```bash
$ rg -n "^(type|func) " internal cmd
cmd/rpc-framing/main.go:11:func main() {
internal/rpc/rpc.go:15:type request struct {
internal/rpc/rpc.go:22:type response struct {
internal/rpc/rpc.go:29:type Handler func(context.Context, json.RawMessage) (any, error)
internal/rpc/rpc.go:31:type Server struct {
internal/rpc/rpc.go:39:func NewServer(addr string) *Server {
internal/rpc/rpc.go:47:func (server *Server) Register(method string, handler Handler) {
internal/rpc/rpc.go:51:func (server *Server) Start() error {
internal/rpc/rpc.go:73:func (server *Server) Addr() string {
internal/rpc/rpc.go:80:func (server *Server) Close() error {
internal/rpc/rpc.go:94:func (server *Server) handleConn(conn net.Conn) {
internal/rpc/rpc.go:123:func (server *Server) dispatch(conn net.Conn, req request) {
internal/rpc/rpc.go:149:func (server *Server) writeResponse(conn net.Conn, resp response) {
internal/rpc/rpc.go:157:type pendingCall struct {
internal/rpc/rpc.go:161:type Client struct {
internal/rpc/rpc.go:172:func NewClient(addr string) *Client {
internal/rpc/rpc.go:181:func (client *Client) Connect() error {
internal/rpc/rpc.go:191:func (client *Client) Close() error {
internal/rpc/rpc.go:204:func (client *Client) Call(ctx context.Context, method string, params any, out any) error {
internal/rpc/rpc.go:252:func (client *Client) readLoop() {
internal/rpc/rpc.go:288:func (client *Client) failPending(correlationID string, err error) {
internal/rpc/rpc.go:300:func (client *Client) failAll(err error) {
internal/framing/framing.go:9:func Encode(message any) ([]byte, error) {
internal/framing/framing.go:20:type Decoder struct {
internal/framing/framing.go:24:func (decoder *Decoder) Feed(chunk []byte) ([][]byte, error) {
```

검증 신호:

- `Encode` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Decoder`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```go
func Encode(message any) ([]byte, error) {
	payload, err := json.Marshal(message)
	if err != nil {
		return nil, err
	}
	frame := make([]byte, 4+len(payload))
	binary.BigEndian.PutUint32(frame[0:4], uint32(len(payload)))
	copy(frame[4:], payload)
	return frame, nil
}
```

왜 이 코드가 중요했는가:

`Encode`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Decoder`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
