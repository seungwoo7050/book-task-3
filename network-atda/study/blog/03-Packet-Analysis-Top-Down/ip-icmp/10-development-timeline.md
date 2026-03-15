# IP and ICMP Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 IPv4 header를 한 번에 다 해석하는 방식이 아니다. 먼저 TTL-limited probe로 path discovery를 보고, 그다음 fragmentation trace로 datagram 분해와 재조립을 읽는 식으로 네트워크 계층 역할을 단계적으로 넓힌다. 전환점은 네 번이다.

## 1. traceroute trace는 Echo Request보다 TTL ladder를 먼저 읽어야 한다

frame `1`, `3`, `5`는 모두 `ICMP Echo Request`지만, 현재 답안이 먼저 보는 것은 payload가 아니라 TTL이다. 값은 `1 -> 2 -> 3`으로 증가한다. 이 한 줄 때문에 probe는 단순 ping이 아니라, hop-by-hop path discovery를 위한 실험 장치가 된다.

즉 이 lab의 첫 단계는 ICMP message type보다 IP header의 TTL이 path exploration의 스위치 역할을 한다는 점을 확인하는 것이다.

## 2. router ICMP가 "실패"가 아니라 route discovery evidence가 된다

frame `2`와 `4`는 `Time Exceeded (11/0)`다. 출발점이었던 Echo Request가 router에서 만료되면서, 이제 router 자신의 source IP가 바깥 IP header에 드러난다. 현재 trace에서는 그 주소가 `10.0.0.1`, `172.16.0.1`이다.

그래서 traceroute는 destination까지 바로 가지 못한 probe를 실패로 읽지 않는다. 오히려 그 intermediate ICMP가 각 hop의 존재를 알려 주는 핵심 증거가 된다.

## 3. destination에 닿는 순간 ICMP semantics가 다시 바뀐다

frame `6`은 `Echo Reply (0/0)`다. TTL-limited intermediate response가 아니라 실제 destination `93.184.216.34`가 응답했다는 뜻이다. 이 전환 때문에 같은 ICMP라도 router-generated control message와 endpoint-generated success signal을 서로 다른 역할로 읽게 된다.

결국 traceroute section은 IP header와 ICMP가 함께 route discovery protocol처럼 동작하는 장면으로 닫힌다.

## 4. fragmentation trace는 하나의 datagram이 세 조각으로 나뉘는 물리적 흔적을 보여 준다

두 번째 trace에서는 focus가 경로에서 datagram 구조로 옮겨간다. frames `1/2/3`은 모두 `ip.id=0x3039`를 공유하고 `MF`는 `1/1/0`, `offset`은 `0/175/350`이다. `offset*8`을 적용하면 byte 시작점이 `0/1400/2800`이 되고, 마지막 fragment 길이 `728`을 통해 전체 payload 3508 bytes까지 재구성할 수 있다.

이 단계 덕분에 fragmentation은 "패킷이 쪼개진다"는 말보다, 어떤 필드 조합으로 조각을 다시 맞추는지까지 구체화된다. 현재 answer markdown가 Wireshark reassembly hint와 함께 manual byte range 계산을 적는 이유도 여기에 있다.

## 지금 남는 한계

이 자료는 교육용 trace라 홉 수, fragment 수, IPv4 field 값이 모두 작고 깔끔하다. IPv6 extension header, PMTUD negotiation, 다양한 traceroute implementation 차이는 현재 범위 밖이다. 그래도 TTL ladder와 fragment chain이라는 두 핵심 장면은 충분히 선명하게 남아 있다.
