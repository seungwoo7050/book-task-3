# IP and ICMP Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `IP and ICMP Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 trace를 분석해 IPv4 header 구조, fragmentation, TTL 동작, ICMP 메시지 type/code를 이해하고, 이들이 `ping`과 `traceroute`에서 어떤 의미를 갖는지 정리합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `ip-traceroute.pcapng` | Traceroute | 원격 호스트로 가는 traceroute 과정에서 발생한 ICMP trace |
| `ip-fragmentation.pcapng` | Fragmentation | 큰 ICMP 패킷으로 인해 IP fragmentation이 일어난 trace |

## 풀어야 할 질문

### 파트 1. IPv4 헤더 (`ip-traceroute.pcapng`)

1. 첫 번째 ICMP Echo Request의 IP version, header length, total length는 무엇입니까?
2. `Identification`, `Flags`, `Fragment Offset` 값은 무엇이며 fragmentation과 어떤 관계가 있습니까?
3. `TTL` 값은 얼마이며, `Protocol` field는 무엇을 뜻합니까?
4. source IP와 destination IP는 무엇입니까?
5. TTL을 증가시키며 보낸 successive Echo Request들을 보면 TTL과 `Identification` 값은 어떻게 변합니까?
6. 첫 번째 `ICMP Time Exceeded` 메시지의 source IP, TTL, ICMP type/code는 무엇입니까?
7. successive Echo Request들의 `Identification` 값은 같습니까, 다릅니까? 왜 그렇다고 볼 수 있습니까?
8. source IP 기준으로 정렬했을 때 `ICMP Time Exceeded`를 보낸 서로 다른 IP 주소는 몇 개입니까? 이것이 무엇을 의미합니까?

### 파트 2. IP Fragmentation (`ip-fragmentation.pcapng`)

1. 처음으로 fragmentation이 일어난 ICMP Echo Request의 `Identification`은 무엇이며, 각 fragment의 `Flags`와 `Fragment Offset`은 무엇입니까?
2. 하나의 원본 datagram이 몇 개의 fragment로 나뉘었습니까? 같은 datagram에서 왔다는 사실은 어떻게 확인합니까?
3. fragment들 사이에서 IP header의 어떤 field는 바뀌고 어떤 field는 유지됩니까?
4. 각 fragment의 `Total Length`와 `Fragment Offset x 8` 값을 계산해 원래 datagram 전체를 설명할 수 있습니까?
5. `More Fragments (MF)` flag 값은 각 fragment에서 어떻게 나타납니까? MF=0인 fragment는 어느 것입니까?
6. IP reassembly는 어떻게 이루어지며, reassembly는 라우터가 합니까, 목적지 호스트가 합니까? Wireshark는 이를 어떻게 표시합니까?

### 파트 3. ICMP 메시지

1. Echo Request의 ICMP Type/Code는 무엇입니까? Echo Reply는 무엇입니까?
2. `Time Exceeded` 메시지의 ICMP Type/Code는 무엇이며 어떤 상황을 뜻합니까?
3. Echo Request와 Echo Reply는 같은 `Identifier`와 `Sequence Number`를 공유합니까? 이 field들의 목적은 무엇입니까?
4. Echo Request payload에는 몇 바이트의 데이터가 들어 있습니까? enclosing IP datagram의 Total Length와 어떤 관계가 있습니까?

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
