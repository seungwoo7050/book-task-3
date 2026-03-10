# Traceroute — TTL을 조작해 경로를 추적하다

## ICMP 핑에서 한 걸음 더

ICMP 핑은 "목적지에 도달하는가"를 확인하는 도구였다. Traceroute는 "목적지까지 **어떤 경로를 거쳐서** 가는가"를 보여주는 도구다.

원리는 IP 프로토콜의 TTL(Time To Live) 필드를 이용한다. TTL은 원래 패킷이 네트워크에서 무한 루프를 도는 걸 방지하기 위한 메커니즘이다. 라우터를 하나 지날 때마다 TTL이 1씩 줄어들고, 0이 되면 라우터가 패킷을 버리면서 **ICMP Time Exceeded** 메시지를 원래 보낸 사람에게 돌려보낸다.

Traceroute는 이걸 역이용한다. TTL을 1로 설정한 패킷을 보내면 첫 번째 라우터에서 만료되고, 그 라우터의 IP 주소를 알 수 있다. TTL을 2로 올리면 두 번째 라우터. 이걸 반복하면 전체 경로가 드러난다.

## UDP probe + ICMP 수신: 두 종류의 소켓

이 구현에서는 **두 개의 소켓**을 사용한다:

1. **UDP 소켓** (전송용): TTL을 설정한 UDP 패킷을 목적지로 보낸다
2. **Raw ICMP 소켓** (수신용): 라우터가 보내주는 ICMP 응답을 받는다

왜 ICMP echo request가 아니라 UDP를 쓸까? 전통적인 Unix traceroute가 UDP를 사용한다. 도달할 수 없는 높은 포트 번호(33434~)로 보내면, 목적지에 도달했을 때 **ICMP Port Unreachable**(type=3, code=3)이 돌아온다. 이걸로 "목적지에 도착했다"는 걸 알 수 있다.

```python
send_socket = socket.socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
send_socket.setsockopt(IPPROTO_IP, IP_TTL, ttl)

recv_socket = socket.socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
```

## probe 매칭: 어떤 ICMP 응답이 내 probe의 것인지

한 TTL에 여러 probe를 보내고(기본 3개), 각각의 RTT를 측정한다. 문제는 ICMP 응답이 **어떤 probe에 대한 것인지** 구분해야 한다는 것이다.

핵심은 ICMP Time Exceeded 메시지 안에 **원본 패킷의 일부가 포함**되어 있다는 점이다. ICMP 에러 메시지는 원래 IP 패킷의 처음 일부를 그대로 실어 보낸다. 이 안에 UDP 헤더가 있고, 거기서 목적지 포트 번호를 읽을 수 있다.

그래서 각 probe마다 고유한 목적지 포트를 사용했다:

```python
def build_probe_port(ttl, probe_index, probes_per_hop, base_port=33434):
    return base_port + (ttl - 1) * probes_per_hop + probe_index
```

ICMP 응답에서 원본 UDP의 목적지 포트를 추출하고, 내가 보낸 포트와 비교하면 매칭이 된다.

## ICMP 응답 파싱의 깊이

ICMP Time Exceeded 응답의 구조는 이렇다:
```
[IP 헤더] [ICMP 헤더(8B): type=11, code=0] [원본 IP 헤더] [원본 UDP 헤더]
```

파싱해야 할 레이어가 **세 겹**이다:
1. 외층 IP 헤더 → IHL로 건너뛰기
2. ICMP 헤더 → type, code 읽기, 8바이트 건너뛰기
3. 내장된 원본 IP 헤더 → IHL로 건너뛰기
4. 원본 UDP 헤더 → source port, destination port 읽기

```python
def parse_icmp_response(packet):
    ip_header_len = (packet[0] & 0x0F) * 4
    icmp_type = packet[ip_header_len]
    icmp_code = packet[ip_header_len + 1]
    # 원본 IP/UDP는 ICMP 헤더(8B) 뒤에 있음
    embedded_ip_offset = ip_header_len + 8
    embedded_ip_header_len = (packet[embedded_ip_offset] & 0x0F) * 4
    udp_offset = embedded_ip_offset + embedded_ip_header_len
    _, dest_port = struct.unpack("!HH", packet[udp_offset:udp_offset + 4])
```

ICMP 핑에서도 IP 헤더 파싱을 했지만, traceroute에서는 **중첩된 패킷 구조**를 파싱해야 해서 한 차원 더 복잡했다. 이 경험은 나중에 Wireshark 패킷 분석 과제에서 패킷 구조를 읽는 데 크게 도움이 됐다.

## 종료 조건: Port Unreachable

TTL을 충분히 올리면 패킷이 실제 목적지에 도달한다. 목적지에서는 UDP 포트 33434+ 같은 곳에 아무 서비스도 없으니, **ICMP Port Unreachable** (type=3, code=3)을 보낸다.

```python
if any(
    obs.responder == destination_ip
    and obs.icmp_type == 3
    and obs.icmp_code == 3
    for obs in observations
):
    break  # 목적지 도달, trace 종료
```

이 종료 조건 없이는 `max_hops`까지 무조건 반복한다.

## hop별 출력 포맷

출력은 시스템 `traceroute` 명령과 유사한 형식을 따랐다:

```
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max
 1  1.234 ms  1.567 ms  1.345 ms  192.168.1.1
 2  5.678 ms  *  6.012 ms  10.0.0.1
 3  12.345 ms  11.890 ms  12.567 ms  8.8.8.8
```

`*`는 해당 probe에 응답이 없었음(타임아웃)을 의미한다. 같은 hop에서 다른 IP가 응답할 수도 있는데(ECMP 로드밸런싱), 이 경우 여러 IP를 `/`로 구분해서 표시한다.

## 테스트 전략

ICMP 핑과 마찬가지로 두 계층 테스트:

```bash
# 비권한 테스트: 패킷 파싱, 포트 빌드, hop 포맷 검증
make -C problem test

# Live 테스트: 실제 traceroute 수행 (root 필요)
sudo make -C problem run-client HOST=8.8.8.8
```

## 이 과제에서 가져간 것

"TTL은 hop count 제한 용도"라는 교과서 설명은 알고 있었지만, 이걸 역이용해서 경로를 탐색하는 아이디어는 직접 구현해봐야 체감된다. ICMP 에러 메시지 안에 원본 패킷이 들어있다는 사실도, 실제로 바이트를 파싱하면서 비로소 "아, 이래서 probe 매칭이 되는구나"라고 이해했다.

이 과제는 ICMP 핑의 자연스러운 확장이었고, 다음에 올 Distance-Vector 라우팅 과제를 위한 워밍업이기도 했다. 패킷이 어떤 경로를 거쳐가는지를 직접 확인해본 뒤에, "그 경로를 어떻게 정하는가"를 구현하는 순서가 자연스러웠다.

---

> **학습 키워드**: TTL, ICMP Time Exceeded (type=11), ICMP Port Unreachable (type=3), UDP probe, 중첩 패킷 파싱, `IP_TTL` 소켓 옵션, probe 매칭, hop-by-hop tracing