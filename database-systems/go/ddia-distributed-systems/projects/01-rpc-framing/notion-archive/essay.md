# RPC Framing — 바이트의 강에서 메시지를 건져 올리기

## 들어가며

분산 시스템 시리즈의 첫 번째 프로젝트다. 앞선 database-internals 시리즈가 "한 대의 머신 안에서 데이터를 어떻게 다루는가"를 탐구했다면, 이 시리즈는 "여러 머신이 어떻게 소통하는가"에 답한다. 모든 분산 시스템의 근간에는 네트워크 통신이 있고, 그 네트워크 통신의 가장 기초적인 문제가 바로 **프레이밍(framing)**이다.

TCP가 제공하는 것은 "신뢰할 수 있는 바이트 스트림"이다. 순서가 보장되고, 유실되면 재전송된다. 하지만 TCP는 메시지 경계를 모른다. `Write("hello")`를 두 번 호출했더라도, 상대방은 `"hellohe"` + `"llo"` 처럼 전혀 다른 단위로 받을 수 있다. 이 문제를 해결하지 않으면, 그 위에 어떤 프로토콜을 올려도 제대로 동작하지 않는다.

## 프레이밍: 길이 접두사 방식

메시지 경계를 복원하는 방법은 여러 가지다. 줄바꿈 구분자(HTTP/1.0), 특수 바이트 시퀀스(WebSocket), 고정 길이, 그리고 **길이 접두사(length prefix)**. 이 프로젝트는 가장 깔끔한 길이 접두사 방식을 선택한다.

```
[4-byte big-endian payload length][JSON payload]
```

인코딩은 단순하다:

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

JSON으로 직렬화하고, 앞에 4바이트로 길이를 붙인다. 이게 한 프레임이다.

## 디코더: 불완전한 세계에서의 파싱

인코딩보다 디코딩이 훨씬 어렵다. TCP 스트림에서 읽은 chunk가 정확히 프레임 하나를 담고 있을 거라는 보장이 없기 때문이다.

세 가지 상황을 처리해야 한다:
1. **한 chunk에 프레임 하나**: 깔끔하게 하나 반환
2. **한 chunk에 프레임 여러 개**: 전부 추출
3. **프레임이 chunk 경계에 걸침(split chunk)**: 버퍼에 보관하고 다음 chunk를 기다림

`Decoder`는 내부 `buffer`에 chunk를 누적하면서 이 세 상황을 모두 처리한다:

```go
func (decoder *Decoder) Feed(chunk []byte) ([][]byte, error) {
    decoder.buffer = append(decoder.buffer, chunk...)
    messages := make([][]byte, 0)

    for len(decoder.buffer) >= 4 {
        payloadLength := binary.BigEndian.Uint32(decoder.buffer[0:4])
        totalLength := int(4 + payloadLength)
        if totalLength < 4 {
            return nil, errors.New("framing: invalid frame length")
        }
        if len(decoder.buffer) < totalLength {
            break
        }
        payload := append([]byte(nil), decoder.buffer[4:totalLength]...)
        messages = append(messages, payload)
        decoder.buffer = append([]byte(nil), decoder.buffer[totalLength:]...)
    }
    return messages, nil
}
```

핵심은 `for` 루프다. 버퍼에 데이터가 충분할 때까지 반복하며, 부족하면 `break`하고 나중을 기다린다. `append([]byte(nil), ...)` 패턴은 슬라이스를 복사하여 원본 버퍼와의 메모리 공유를 끊는 방어적 코딩이다.

## RPC 계층: 메시지에 의미를 부여하다

프레이밍이 "바이트 → 메시지"를 해결했다면, RPC 계층은 "메시지 → 원격 함수 호출"을 해결한다. 요청과 응답의 형태를 정의한다:

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

`CorrelationID`가 이 설계의 핵심이다. 클라이언트가 여러 요청을 동시에 보낼 때, 응답이 요청 순서와 다르게 도착할 수 있다. 각 요청에 고유 ID를 붙이고, 응답에도 같은 ID를 실어 보내면, 어떤 응답이 어떤 요청의 것인지 매칭할 수 있다.

## 서버: 핸들러 등록과 디스패치

서버는 세 가지 책임을 진다: TCP 연결 수락, 프레임 디코딩, 핸들러 디스패치.

```go
func (server *Server) handleConn(conn net.Conn) {
    decoder := &framing.Decoder{}
    buffer := make([]byte, 4096)
    for {
        n, err := conn.Read(buffer)
        if err != nil {
            return
        }
        payloads, err := decoder.Feed(buffer[:n])
        for _, payload := range payloads {
            var req request
            json.Unmarshal(payload, &req)
            go server.dispatch(conn, req)
        }
    }
}
```

연결마다 자체 `Decoder`를 갖는다. 프레이밍은 연결 단위의 상태이기 때문이다. 각 요청은 별도 goroutine으로 처리하여 한 요청의 느린 처리가 같은 연결의 다른 요청을 막지 않게 한다.

디스패치는 메서드 이름으로 핸들러를 찾고, 없으면 `unknown method` 에러를 반환한다. 핸들러 실행 중 에러가 발생하면 에러 응답을 보낸다. 모든 경우에 대해 응답을 보내는 것이 중요하다—클라이언트의 pending call이 영원히 대기하지 않도록.

## 클라이언트: Pending Call Map

클라이언트의 핵심 자료구조는 `pending map[string]pendingCall`이다. 각 `pendingCall`은 응답을 전달할 채널을 가진다.

```go
type pendingCall struct {
    response chan response
}
```

`Call` 메서드의 동작:
1. 고유한 `correlation_id` 생성 (`atomic.AddUint64`)
2. pending map에 등록
3. 요청 프레임 전송
4. `select`로 세 가지를 동시에 기다림: 응답 도착, context 타임아웃, 연결 종료

```go
select {
case resp := <-call.response:
    // 응답 처리
case <-ctx.Done():
    // 타임아웃
case <-client.closed:
    // 연결 끊김
}
```

`readLoop` goroutine은 서버로부터 도착하는 프레임을 계속 읽으며, correlation ID로 해당하는 pending call을 찾아 채널에 응답을 넣어준다.

연결이 끊기면 `failAll`이 호출되어 모든 남은 pending call에 에러를 전파한다. 이렇게 하지 않으면 `Call`이 영원히 블로킹된다.

## 동시성 안전

`Server`와 `Client` 모두 `sync.Mutex`로 공유 상태를 보호한다:
- 서버: `conns` 맵 (활성 연결 추적)
- 클라이언트: `pending` 맵 (진행 중인 호출 추적)

`nextID`는 `atomic.AddUint64`로 동기화하여 mutex 없이 ID를 생성한다.

## 테스트가 증명하는 것들

5개 테스트가 프레이밍과 RPC의 핵심 시나리오를 검증한다:

1. **DecoderHandlesSingleMessage**: 단일 프레임 인코딩-디코딩 왕복
2. **DecoderHandlesSplitChunks**: 프레임을 반으로 쪼개 보내도 정상 디코딩
3. **RPCServerClientRoundTrip**: echo 핸들러를 통한 요청-응답 왕복
4. **RPCHandlesConcurrentCalls**: 3개의 동시 요청이 각각 올바른 결과를 받음
5. **RPCPropagatesServerErrorsAndTimeout**: 서버 에러 전파 + 클라이언트 타임아웃

특히 테스트 4번이 이 프로젝트의 존재 이유를 증명한다. correlation ID 없이는 동시 요청의 응답을 올바른 caller에게 돌려줄 수 없다.

## 돌아보며

이 프로젝트는 분산 시스템의 "0층"이다. TCP 위에 메시지 경계를 복원하고, 그 위에 RPC 의미를 부여하는 것. 이 두 계층이 없으면 이후의 replication, sharding, consensus 어느 것도 구현할 수 없다. gRPC나 Thrift 같은 프레임워크가 당연하게 해주는 일을, 손수 구현함으로써 그 아래에서 무슨 일이 벌어지는지 직접 확인했다.
