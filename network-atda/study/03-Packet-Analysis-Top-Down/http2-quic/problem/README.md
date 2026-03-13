# HTTP/2 and QUIC Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `HTTP/2 and QUIC Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. raw pcap을 모두 들여다보기보다, trace에서 뽑아 낸 condensed dataset을 근거로 비교 포인트를 분명하게 잡는 데 초점을 둡니다.

## 문제 목표

- HTTP/2 frame interleaving을 stream 단위로 설명한다.
- QUIC handshake packet type, packet number, connection ID를 설명한다.
- 둘의 multiplexing / head-of-line tradeoff를 비교한다.

## 제공 trace

| 파일 | 설명 |
| :--- | :--- |
| `http2-trace.tsv` | HTTP/2 stream 1, 3의 interleaving과 `WINDOW_UPDATE`가 담긴 condensed trace |
| `quic-trace.tsv` | QUIC `Initial`, `Handshake`, `1-RTT`, stream 4/8, connection ID가 담긴 condensed trace |

## 풀어야 할 질문

### Part 1. HTTP/2

1. 어떤 transport 위에서 동작하는가?
2. 어떤 signal이 HTTP/2 협상을 보여 주는가?
3. 어떤 stream ID가 application request를 실어 나르는가?
4. 어떤 frame sequence가 multiplexing을 보여 주는가?
5. 어떤 connection-level frame이 flow control을 보여 주는가?
6. HTTP/2는 모든 head-of-line blocking을 제거하는가?

### Part 2. QUIC

7. 어떤 transport 위에서 동작하는가?
8. 어떤 packet type이 handshake와 data 전환을 보여 주는가?
9. 어떤 connection ID가 보이는가?
10. 어떤 stream ID가 application data를 운반하는가?
11. packet number는 무엇을 보여 주는가?
12. HTTP/2와 비교했을 때 가장 중요한 구조 차이는 무엇인가?

## 성공 기준

- 총 12개 질문에 모두 답한다.
- frame 번호, stream ID, packet type, connection ID 같은 근거를 직접 적는다.
- HTTP/2와 QUIC의 차이를 단순 "더 빠르다"가 아니라 구조 차이로 설명한다.
