# Ethernet and ARP Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 많은 packet을 샅샅이 뒤지는 분석이 아니다. 오히려 단 3 frame을 끊어 읽으면서, IP 주소가 실제 Ethernet destination으로 바뀌기까지의 문턱을 순서대로 복원하는 방식에 가깝다. 전환점은 세 번으로 명확하다.

## 1. 먼저 broadcast ARP request로 "누가 192.168.0.1인가"를 묻는다

frame `1`은 이 lab의 출발점이다. Ethernet destination이 `ff:ff:ff:ff:ff:ff`라서 LAN 전체에 뿌려지고, ARP payload 안에는 sender IP `192.168.0.2`, target IP `192.168.0.1`, target MAC `00:00:00:00:00:00`가 들어 있다. 즉 requester는 상대 IP는 알지만 MAC은 아직 모른다는 사실을 frame 하나가 그대로 보여 준다.

이 단계 덕분에 ARP는 "주소 변환 프로토콜"이라는 설명보다 "모르는 MAC을 broadcast로 찾는 discovery 단계"로 더 선명해진다.

## 2. reply는 broadcast를 멈추고 requester에게 바로 되돌아간다

frame `2`는 같은 LAN 안에서 응답이 왜 unicast가 되는지 보여 준다. sender MAC `66:77:88:99:aa:bb`, sender IP `192.168.0.1`가 자기 정체를 밝히고, Ethernet destination은 처음 요청을 보낸 `00:11:22:33:44:55`로 바로 향한다. ARP reply는 "정답을 모두에게 다시 알리는" 단계가 아니라, requester 하나에게 필요한 mapping을 돌려주는 단계라는 점이 여기서 분명해진다.

따라서 이 lab의 핵심은 request/reply 모두 ARP라는 사실보다, 주소 해석의 discovery와 answer phase가 Ethernet destination 정책부터 다르다는 데 있다.

## 3. 다음 IPv4 frame이 같은 MAC을 실제로 사용하면서 handoff가 끝난다

frame `3`은 EtherType이 `0x0800`으로 바뀐 IPv4 frame이다. 중요한 건 destination MAC이 frame `2`에서 알려 준 `66:77:88:99:aa:bb`와 일치한다는 점이다. 여기서 처음으로 "ARP가 실제로 다음 L3 packet delivery를 열었다"는 문장을 근거 있게 쓸 수 있다.

즉 이 lab는 ARP reply까지가 끝이 아니다. 그 뒤 첫 IPv4 frame까지 확인해야만, address resolution이 이론이 아니라 실제 forwarding prerequisite였음을 닫을 수 있다.

## 지금 남는 한계

trace가 너무 작아서 HTTP payload offset, cache aging, spoofing, gratuitous ARP 같은 확장 질문은 여기서 답할 수 없다. 그래서 이 문서는 Ethernet/ARP 전체 교재를 대체하기보다, 최소 trace에서 주소 해석 handoff를 읽는 기준점을 세우는 문서로 남기는 편이 정확하다.
