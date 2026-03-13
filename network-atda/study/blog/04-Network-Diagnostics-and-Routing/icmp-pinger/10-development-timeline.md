# ICMP Pinger 개발 타임라인

## Day 1 — checksum부터 잡고, packet을 조립한다

### Session 1

- 목표: live ping을 바로 실행하려는 충동을 억제하고, 먼저 packet build와 checksum을 비권한 환경에서 고정한다.
- 진행: skeleton을 열어 빈 구간을 보고, `test_icmp_pinger.py`를 먼저 읽었다. `TestInternetChecksum`과 `TestPacketBuilding` 두 클래스가 각각 RFC 1071과 ICMP header 포맷을 독립적으로 따진다.
- 이슈: 처음에는 `socket.SOCK_RAW`를 열면 프로젝트 절반이 해결된다고 생각했다. 하지만 checksum이 틀리면 OS가 패킷을 버리거나 응답이 아예 오지 않아 무엇이 문제인지 알 수 없다. 그래서 live 실행보다 checksum 정확성이 먼저였다.

핵심 코드:

```py
# checksum 없이 임시 header 조립
header = struct.pack(
    ICMP_HEADER_FORMAT,
    ICMP_ECHO_REQUEST,
    0,
    0,            # checksum placeholder
    identifier,
    sequence,
)
payload = struct.pack("!d", time.time())
checksum = internet_checksum(header + payload)

# checksum을 넣고 최종 header 재조립
header = struct.pack(
    ICMP_HEADER_FORMAT,
    ICMP_ECHO_REQUEST,
    0,
    checksum,
    identifier,
    sequence,
)
```

- 메모: 이 two-pass assembly 패턴이 없으면, checksum을 계산하기 위해 checksum 자리가 0이어야 한다는 RFC 1071 요건을 위반한다. 테스트 `test_checksum_valid`는 완성 packet 전체로 재계산했을 때 0이 나와야 한다고 단언한다.

### Session 2

- 목표: raw reply에서 ICMP payload를 정확히 잘라 내는 로직을 완성한다.
- 진행: raw socket reply는 IPv4 header + ICMP header + payload 형태로 온다. IHL(header length)은 첫 바이트 하위 4비트에 4를 곱해 구한다.
- 이슈: 처음에는 reply 바이트를 바로 ICMP 헤더로 파싱했다가, 앞에 IP header가 붙어 있어서 type/code가 엉뚱한 값이 나왔다. `ip_header_len = (data[0] & 0x0F) * 4`가 유일한 이유로 맨 처음 해야 할 계산이다.
- 이슈 2: RTT를 재려면 보낸 시각이 payload에 담겨 있어야 한다. payload 첫 8바이트를 `struct.pack("!d", time.time())`으로 묻고, reply에서 꺼내어 `recv_time - send_time`으로 계산한다.

핵심 코드:

```py
ip_header_len = (data[0] & 0x0F) * 4
icmp_data = data[ip_header_len:]
icmp_type, code, checksum, pkt_id, sequence = struct.unpack(
    ICMP_HEADER_FORMAT, icmp_data[:ICMP_HEADER_SIZE]
)
if icmp_type != ICMP_ECHO_REPLY or pkt_id != identifier:
    return None
send_time = struct.unpack("!d", icmp_data[ICMP_HEADER_SIZE:ICMP_HEADER_SIZE + 8])[0]
```

```bash
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
    study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py
# 7 passed
```

### Session 3

- 목표: live 실행 경계를 정리하고, 최종 통계 출력을 완성한다.
- 진행: live raw socket은 root/admin 권한이 필요하다. `PermissionError`를 잡아서 안내 메시지를 띄운다. 1초 간격 ping 흐름에서 마지막 ping 이후 sleep이 필요 없다는 점은 `FakeClock` 기반 테스트에서 검증됐다. RTT 통계(`min/avg/max`)는 loss가 있을 때 skip된다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
7 passed
```

```bash
$ sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=8.8.8.8
PING 8.8.8.8 (8.8.8.8): 16 bytes of data

16 bytes from 8.8.8.8: icmp_seq=1  RTT=12.345 ms
16 bytes from 8.8.8.8: icmp_seq=2  RTT=11.876 ms
16 bytes from 8.8.8.8: icmp_seq=3  RTT=12.123 ms
16 bytes from 8.8.8.8: icmp_seq=4  RTT=12.001 ms

--- 8.8.8.8 ping statistics ---
4 packets sent, 4 received, 0.0% loss
RTT min/avg/max = 11.876/12.086/12.345 ms
```

- 정리:
  - checksum은 packet build와 분리해서 구현하면 안 된다. two-pass assembly가 RFC 1071의 요구 사항을 자연스럽게 충족한다.
  - raw reply에서 IP header를 먼저 건너뛰는 것이 ICMP parsing의 첫 번째 규칙이다.
  - live 실행과 fake-socket 테스트는 각각 다른 것을 검증한다. live는 "OS와 네트워크가 반응하는가", fake는 "packet 조립/파싱이 계약대로 동작하는가"다.
