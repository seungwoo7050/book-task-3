# 20 01 RPC Framing의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Encode`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing/framing.go`의 `Encode`
- 처음 가설:
  `Encode` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Encode|Decoder" internal cmd`로 핵심 함수 위치를 다시 잡고, `Encode`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Encode|Decoder" internal cmd
internal/rpc/rpc.go:102:	decoder := &framing.Decoder{}
internal/rpc/rpc.go:150:	frame, err := framing.Encode(resp)
internal/rpc/rpc.go:164:	decoder *framing.Decoder
internal/rpc/rpc.go:175:		decoder: &framing.Decoder{},
internal/rpc/rpc.go:220:	frame, err := framing.Encode(request{
internal/framing/framing.go:9:func Encode(message any) ([]byte, error) {
internal/framing/framing.go:20:type Decoder struct {
internal/framing/framing.go:24:func (decoder *Decoder) Feed(chunk []byte) ([][]byte, error) {
```

검증 신호:

- `Encode` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `TCP stream에서 message boundary를 복구하는 방법을 익힙니다.`

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

`Encode`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음:

- `Decoder`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Decoder`가 `Encode`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing/framing.go`의 `Decoder`
- 처음 가설:
  `Decoder`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Encode`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

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

- `Decoder`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `TestRPCPropagatesServerErrorsAndTimeout` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```go
type Decoder struct {
	buffer []byte
}

func (decoder *Decoder) Feed(chunk []byte) ([][]byte, error) {
	decoder.buffer = append(decoder.buffer, chunk...)
	messages := make([][]byte, 0)

	for len(decoder.buffer) >= 4 {
		payloadLength := binary.BigEndian.Uint32(decoder.buffer[0:4])
		totalLength := int(4 + payloadLength)
		if totalLength < 4 {
			return nil, errors.New("framing: invalid frame length")
		}
```

왜 이 코드가 중요했는가:

`Decoder`가 없으면 `Encode`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Pending Map`에서 정리한 요점처럼, 동시에 여러 RPC를 보낼 수 있으므로 응답은 요청 순서와 다르게 도착할 수 있다. 그래서 client는 `correlation_id -> pending call` map을 유지한다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
