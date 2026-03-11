# HTTP 버전 비교: HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3

## 개요

HTTP Wireshark 실습에서 관찰한 HTTP/1.1의 특성을 더 넓은 맥락에서 이해하기 위해, HTTP의 주요 버전들을 비교한다.

## 버전별 핵심 특성

| 특성 | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
| :--- | :--- | :--- | :--- | :--- |
| 연결 관리 | 요청마다 새 TCP | 지속 연결 기본 | 멀티플렉싱 | QUIC (UDP 기반) |
| HOL 블로킹 | 해당 없음 | 존재 | TCP 레벨만 | 없음 |
| 헤더 형식 | 텍스트 | 텍스트 | 바이너리 (HPACK) | 바이너리 (QPACK) |
| 서버 푸시 | 없음 | 없음 | 지원 | 지원 |
| 우선순위 | 없음 | 없음 | 스트림 우선순위 | 스트림 우선순위 |
| TLS | 선택 | 선택 | 사실상 필수 | 내장 |

## HTTP/1.0 → HTTP/1.1 (실습 관찰 대상)

### 지속 연결 (Persistent Connection)

HTTP/1.0: 요청마다 TCP 3-way handshake를 수행
```
Client → SYN → Server
Client ← SYN-ACK ← Server
Client → ACK → Server
Client → GET /page.html → Server
Client ← 200 OK ← Server
Client → FIN → Server     ← 연결 종료!

Client → SYN → Server     ← 새 연결!
Client → GET /image.png → Server
...
```

HTTP/1.1: `Connection: keep-alive`로 연결 재사용
```
Client → SYN → SYN-ACK → ACK    ← 한 번만!
Client → GET /page.html → Server
Client ← 200 OK ← Server
Client → GET /image.png → Server  ← 같은 연결!
Client ← 200 OK ← Server
Client → GET /style.css → Server  ← 같은 연결!
...
```

**실습에서 확인**: Part 4 (Embedded Objects)에서 기본 HTML과 이미지들이 동일 TCP 연결에서 전송되는 것을 관찰.

### 조건부 GET

HTTP/1.1에서 추가된 캐싱 메커니즘:

```http
# 첫 요청 → 200 OK (전체 응답)
# 두 번째 요청 → If-Modified-Since 포함 → 304 Not Modified (본문 없음)
```

**실습에서 확인**: Part 2 (Conditional GET)에서 304 응답을 관찰.

### Host 헤더

HTTP/1.1에서 `Host` 헤더가 필수가 됨. 이는 **가상 호스팅**(한 IP에서 여러 도메인 운영)을 가능하게 한다.

## HTTP/1.1 → HTTP/2

### HOL(Head-of-Line) 블로킹 문제

HTTP/1.1에서 한 TCP 연결에서 요청은 순차적으로 처리된다:
```
GET /page.html → 응답 대기 → GET /image.png → 응답 대기 → ...
```

큰 파일을 다운로드하면 뒤의 작은 파일들이 대기해야 한다. 브라우저는 이를 우회하기 위해 보통 6~8개의 TCP 연결을 병렬로 열지만, 이는 비효율적이다.

### HTTP/2 멀티플렉싱

HTTP/2는 하나의 TCP 연결에서 여러 **스트림**을 동시에 전송:
```
Stream 1: GET /page.html → 프레임1, 프레임2, ...
Stream 2: GET /image.png → 프레임1, 프레임2, ...  (동시에!)
Stream 3: GET /style.css → 프레임1, 프레임2, ...  (동시에!)
```

### HPACK 헤더 압축

HTTP/1.1은 매 요청마다 동일한 헤더(Host, User-Agent 등)를 텍스트로 반복 전송. HTTP/2는 HPACK 압축으로 헤더 크기를 80-90% 줄인다.

## HTTP/2 → HTTP/3

### TCP의 한계

HTTP/2가 TCP를 사용하므로, TCP 레벨의 HOL 블로킹이 여전히 존재:
- TCP는 순서대로 바이트를 전달
- 한 패킷이 손실되면 뒤의 모든 스트림이 대기

### QUIC 프로토콜

HTTP/3는 UDP 위에 구축된 **QUIC** 프로토콜을 사용:
- 스트림별 독립적 흐름 제어
- 0-RTT 연결 재개
- TLS 1.3 내장

## Wireshark 분석 시사점

실습에서 관찰한 HTTP/1.1 동작을 떠올리며:

| 실습 관찰 | HTTP/2에서의 변화 |
| :--- | :--- |
| 텍스트 헤더가 보임 | 바이너리 프레임으로 인코딩 → 사람이 직접 읽기 어려움 |
| 대용량 문서가 TCP 세그먼트로 분할 | 프레임 단위로 분할, 다른 스트림과 인터리빙 가능 |
| 이미지별 별도 GET 요청 | 서버 푸시로 선제적 전송 가능 |
| 조건부 GET으로 304 응답 | 동일하게 동작 (캐싱은 응용 레벨 최적화) |
