# TCP and UDP Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 transport protocols를 두 장으로 요약하는 식이 아니다. 오히려 TCP trace에서 connection state를 충분히 읽은 뒤, 마지막에 UDP trace로 내려가 "여기에는 왜 그런 state가 안 보이는가"를 비교하는 구조다. 전환점은 네 번이다.

## 1. TCP section은 handshake 세 frame으로 connection state의 문턱을 세운다

frames `1/2/3`은 너무 익숙해서 그냥 넘기기 쉽지만, 현재 답안은 여기서부터 모든 계산을 시작한다. client SYN `seq=0`, server SYN-ACK `ack=1`, client ACK `seq=1 ack=1`이 나오면서 relative sequence numbering과 connection establishment 규칙이 동시에 눈에 보인다.

즉 이 첫 단계는 TCP를 data carrier보다 state machine으로 읽는 문턱이다.

## 2. 이후 data-bearing segments가 byte accounting과 RTT 추정의 재료가 된다

`filter-data` 재실행 결과 frame `4`의 `72 bytes` 이후 6개의 `200-byte` chunk가 이어진다. answer markdown는 이 seq progression을 이용해 총 client transfer `1272 bytes`, RTT `0.19-0.21 ms`, throughput 약 `651,639 B/s`까지 역산한다.

여기서 중요한 건 trace가 짧아도 seq/ack와 timestamp만 있으면 꽤 많은 정량 정보를 끌어낼 수 있다는 점이다.

## 3. clean trace의 한계도 그대로 남긴다

현재 TCP trace에는 retransmission이 없고 `FIN`도 없다. 따라서 loss recovery, teardown, clear slow-start -> congestion avoidance 전환점은 보이지 않는다. 답안은 이 부분을 추정으로 메우지 않고 `not reliably observable`로 남긴다.

이 절제 덕분에 문서는 짧은 trace가 실제로 허락하는 분석 범위를 지킨다.

## 4. 마지막에 UDP trace가 transport minimalism을 드러낸다

UDP section에 들어오면 표면이 확 줄어든다. `udp.length=36` query, `udp.length=62` response, 4개 field, 각 2 bytes라는 사실이 전부다. 그런데 հենց 이 단순함 때문에 TCP와의 대비가 강해진다. handshake도 없고, seq/ack도 없고, 8-byte header 위에 DNS payload만 얹혀 있다.

결국 이 lab의 마지막 전환점은 "TCP에 없는 것이 UDP의 약점"이 아니라, 서로 다른 transport contract가 trace에 얼마나 다른 밀도로 흔적을 남기는지 확인하는 데 있다.

## 지금 남는 한계

자료가 짧고 깨끗해서 congestion event, retransmission, teardown을 직접 볼 수 없다. UDP도 DNS request/reply 2 packet뿐이다. 그래도 handshake, byte accounting, header minimalism이라는 세 축만으로 TCP와 UDP의 성격 차이는 충분히 선명하다.
