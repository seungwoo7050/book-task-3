# TCP and UDP Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `TCP and UDP Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 TCP/UDP trace를 분석해, TCP의 연결 관리와 신뢰성 메커니즘, UDP의 가벼운 datagram 서비스가 어떤 차이를 갖는지 이해합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `tcp-upload.pcapng` | TCP 파일 업로드 | HTTP POST 기반 업로드가 TCP 위에서 진행되는 trace |
| `udp-dns.pcapng` | UDP DNS 트래픽 | DNS query/response가 UDP 위에서 오가는 trace |

## 풀어야 할 질문

### 파트 1. TCP 세그먼트 구조 (`tcp-upload.pcapng`)

1. 클라이언트와 서버의 IP 주소, TCP 포트 번호는 무엇입니까?
2. 연결을 시작하는 TCP SYN 세그먼트의 sequence number는 무엇이며, SYN임을 보여 주는 field는 무엇입니까?
3. 서버가 보낸 SYN-ACK의 sequence number와 acknowledgment number는 무엇이며, ACK 값은 어떻게 결정됩니까?
4. HTTP POST 명령이 들어 있는 TCP 세그먼트의 sequence number와 acknowledgment number는 무엇입니까?
5. 클라이언트가 보낸 처음 여섯 개의 TCP 데이터 세그먼트에 대해 sequence number, payload 바이트 수, 전송 시각, ACK 값을 정리해 보세요.

### 파트 2. TCP 연결 관리

1. trace 전체에서 수신자가 광고한 최소 receive window는 얼마입니까? 0이 되어 송신자를 완전히 멈추게 한 적이 있습니까?
2. 재전송된 세그먼트가 있습니까? 있다면 어떤 근거로 식별할 수 있습니까?
3. 클라이언트는 총 몇 바이트를 서버로 전송했습니까? sequence number로 어떻게 계산할 수 있습니까?
4. TCP 연결 종료는 어떻게 일어납니까? 누가 close를 시작했고 FIN/ACK의 sequence number는 무엇입니까?

### 파트 3. TCP throughput과 RTT

1. 전체 데이터 전송량과 시간 구간을 기준으로 throughput을 계산해 보세요.
2. Wireshark의 TCP Stream Graphs에서 Time-Sequence(Stevens) 그래프를 보면 전송률이 일정합니까, 변합니까?
3. ACK 시각과 세그먼트 전송 시각을 비교해 RTT를 추정해 보세요. RTT는 대략 얼마이며 크게 변합니까?

### 파트 4. TCP 혼잡 제어

1. Time-Sequence 그래프나 Window Scaling 그래프에서 slow start와 congestion avoidance의 전환 지점을 찾을 수 있습니까?
2. 첫 번째 ACK가 오기 전까지 보낸 세그먼트 수를 기준으로 초기 congestion window를 추정할 수 있습니까?

### 파트 5. UDP (`udp-dns.pcapng`)

1. UDP 헤더에는 몇 개의 field가 있으며 각각 이름이 무엇입니까?
2. 각 UDP header field의 길이는 몇 바이트입니까?
3. UDP header의 `Length` field는 무엇을 의미합니까? 실제 패킷으로 확인해 보세요.
4. UDP payload에 이론적으로 담을 수 있는 최대 바이트 수는 얼마입니까?
5. 가능한 가장 큰 source port number는 얼마입니까?
6. IP header에서 UDP의 protocol number는 무엇이며, TCP의 protocol number는 무엇입니까?
7. DNS query와 response로 이루어진 UDP 패킷 쌍을 보고 두 패킷의 포트 번호 관계를 설명해 보세요.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
