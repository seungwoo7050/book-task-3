# Traceroute 개발 타임라인

## Day 1 — probe port 공식, ICMP 계층 해석, 종료 조건

### Session 1

- 목표: TTL 실험보다 probe-reply 매칭 공식을 먼저 독립적으로 고정한다.
- 진행: `test_traceroute.py`의 `TestBuildProbePort`를 먼저 읽었다. TTL 1 probe 0은 port `33434`, TTL 1 probe 1은 `33435`, TTL 2 probe 0은 `33437`이어야 한다는 값이 하드코딩된 expected로 박혀 있었다.
- 이슈: 처음에는 모든 probe에 동일한 `33434`를 써도 된다고 생각했다. 그러나 hop당 3개 probe를 날리면 reply를 받을 때 어느 probe에 대한 응답인지 port 번호로 역추적해야 한다. 동일한 port를 쓰면 이 매칭이 불가능하다.
- 발견: 공식 `base_port + (ttl - 1) * probes_per_hop + probe_index`가 결정론적으로 port를 배분한다. 이 공식 하나가 send script와 recv script를 이어 주는 유일한 계약이다.

핵심 코드:

```py
def build_probe_port(
    ttl: int,
    probe_index: int,
    probes_per_hop: int,
    base_port: int = DEFAULT_BASE_PORT,
) -> int:
    return base_port + (ttl - 1) * probes_per_hop + probe_index
```

```bash
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
    study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py::TestBuildProbePort
# 3 passed
```

### Session 2

- 목표: ICMP reply 안에서 embedded UDP destination port를 꺼내는 parsing 계층을 완성한다.
- 진행: raw recv socket이 받는 packet은 outer IP → ICMP header → embedded IP → embedded UDP 4개 계층이다. 각 계층을 넘어가는 offset이 맞지 않으면 port가 전혀 다른 값이 나온다.
- 이슈: 처음에는 ICMP data를 바로 파싱하면 된다고 생각했다. 실제로는 `outer_ip_len = (data[0] & 0x0F) * 4`로 시작 offset을 구하고, ICMP header 8바이트를 건너뛰고, 그 안의 embedded IP header 길이를 다시 읽어서 embedded UDP destination port에 도달해야 한다.
- 측정: `test_parse_icmp_response`는 각 계층의 실제 바이트를 조립해 넣고, `dest_port`가 의도한 probe port와 일치하는지 단언한다.

핵심 코드:

```py
# ICMP payload 시작점
outer_ip_header_len = (data[0] & 0x0F) * 4
icmp_header = data[outer_ip_header_len : outer_ip_header_len + 8]
icmp_type, icmp_code = icmp_header[0], icmp_header[1]

# embedded IP 안의 embedded UDP
embedded_ip_start = outer_ip_header_len + 8
embedded_ip_header_len = (data[embedded_ip_start] & 0x0F) * 4
udp_start = embedded_ip_start + embedded_ip_header_len
_, dest_port, _, _ = struct.unpack("!HHHH", data[udp_start : udp_start + 8])
```

```bash
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
    study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py::TestParseIcmpResponse
# 2 passed
```

### Session 3

- 목표: 2-socket 아키텍처, `Port Unreachable` 종료 조건, synthetic route 테스트를 완성한다.
- 진행: send side는 `SOCK_DGRAM`으로 TTL을 설정해 보내고, recv side는 raw `SOCK_RAW IPPROTO_ICMP`로 ICMP를 받는다. 같은 socket으로 보내고 받으면 TTL 제어와 raw 수신을 동시에 할 수 없다.
- 이슈: 처음에는 `Time Exceeded`가 오면 hop을 기록하고, destination IP가 응답하면 종료하면 된다고 생각했다. 그러나 destination router가 ICMP `Echo Reply`가 아닌 `Port Unreachable (type 3, code 3)`로 응답한다는 점을 코드에서 명확히 처리해야 했다.
- FakeSocket 설계: `FakeRecvSocket`은 TTL별로 미리 만든 합성 ICMP reply를 큐에 담아 두고, `recv()` 호출마다 하나씩 반환한다. `FakeSendSocket`은 실제 socket 없이 `setsockopt` / `sendto`를 조용히 삼킨다. 이 두 가짜 socket이 있어야 root 없이 전체 경로 추적 흐름을 단위 테스트할 수 있다.

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test
4 passed in 0.01s
```

```bash
$ sudo make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem run-solution HOST=8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 3 probes per hop
  1  192.168.0.1  (192.168.0.1)  1.23 ms  1.45 ms  1.38 ms
  2  10.0.0.1  (10.0.0.1)  4.56 ms  4.78 ms  4.62 ms
  3  *  *  *
  4  8.8.8.8  (8.8.8.8)  12.34 ms  12.01 ms  12.18 ms
```

- 정리:
  - probe-reply 매칭의 유일한 근거는 `build_probe_port`가 만드는 고유 port다. port가 없으면 어느 hop의 응답인지 알 수 없다.
  - ICMP reply는 "맨 바깥 IP → ICMP 헤더 → embedded IP → embedded UDP" 4개 계층이 있다. 계층마다 하나씩 `IHL × 4`를 계산해야 embedded port에 도달한다.
  - 종료 조건은 destination IP가 `Port Unreachable (3/3)`를 보내는 것이다. plain destination IP 비교로는 충분하지 않다.
