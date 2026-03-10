# Ethernet and ARP Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `Ethernet and ARP Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 trace를 분석해 Ethernet frame 구조, MAC addressing, ARP request/reply 교환을 이해하고, LAN에서 IP 주소를 MAC 주소로 해석하는 과정을 설명합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `ethernet-arp.pcapng` | ARP와 Ethernet | LAN 환경의 ARP request/reply와 Ethernet framing이 담긴 trace |

## 풀어야 할 질문

### 파트 1. Ethernet frame 구조

1. ARP request가 담긴 프레임의 48-bit destination MAC 주소는 무엇이며, broadcast입니까 unicast입니까?
2. 같은 프레임의 source MAC 주소는 무엇이며, 어떤 장치에 해당한다고 볼 수 있습니까?
3. `EtherType` field 값은 무엇이며, 어떤 상위 프로토콜을 나타냅니까?
4. HTTP 패킷 안의 ASCII `G`가 Ethernet frame 시작으로부터 몇 바이트 떨어져 나타납니까? Ethernet/IP/TCP header를 합산해 보세요.
5. ARP reply가 담긴 프레임의 destination MAC 주소는 무엇이며, broadcast입니까 unicast입니까?
6. IP datagram을 실은 프레임의 `EtherType`은 무엇이며, ARP frame의 `EtherType`과 어떻게 다릅니까?

### 파트 2. ARP 프로토콜

1. ARP request가 담긴 Ethernet frame의 source/destination MAC 주소(16진수)는 무엇입니까?
2. ARP request의 `opcode` 값은 무엇이며, 어떤 의미입니까?
3. ARP request에는 sender의 IP 주소가 포함되어 있습니까? 있다면 무엇입니까?
4. ARP request가 찾고 있는 target IP 주소는 무엇입니까?
5. ARP request의 target MAC address field는 어떤 값이며, 왜 그런 값입니까?
6. ARP reply의 `opcode` 값은 무엇이며, sender MAC 주소는 무엇입니까?
7. ARP reply를 실은 Ethernet frame의 destination MAC 주소는 무엇이며, 이 주소는 어떻게 결정되었습니까?
8. ARP 교환 뒤 이어지는 IP 패킷이 ARP reply에서 알아낸 MAC 주소를 실제로 사용하고 있는지 확인해 보세요.

### 파트 3. ARP cache

1. 운영체제에서 ARP cache를 보여 주는 명령은 무엇이며, 각 엔트리는 어떤 정보를 담습니까?
2. ARP cache 엔트리의 일반적인 timeout은 어느 정도이며, 만료되면 어떤 일이 일어납니까?
3. ARP cache를 지운 뒤 같은 로컬 호스트에 다시 접근하면 Wireshark에서 어떤 트래픽을 관찰하게 됩니까?

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
