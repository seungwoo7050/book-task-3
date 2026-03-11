# ICMP Pinger vs 시스템 ping — 비교 분석

## 개요

이 문서는 과제에서 구현한 Python ICMP Pinger와 OS 내장 `ping` 유틸리티의 차이를 분석한다.
두 도구 모두 동일한 ICMP Echo Request/Reply 메커니즘을 사용하지만, 구현 세부사항에서 차이가 있다.

## 기능 비교

| 기능 | 과제 구현 (Python) | 시스템 ping |
| :--- | :--- | :--- |
| 프로토콜 | ICMP Echo (Type 8/0) | ICMP Echo (Type 8/0) |
| 소켓 타입 | `SOCK_RAW` | `SOCK_RAW` 또는 `SOCK_DGRAM` |
| 권한 | root/sudo 필수 | setuid root 또는 capabilities |
| Identifier | `os.getpid() & 0xFFFF` | PID 기반 (동일) |
| Payload | 8바이트 (timestamp) | 56바이트 (패턴 + timestamp) |
| 타임아웃 | `select()` 1초 고정 | 설정 가능 (`-W` 옵션) |
| 통계 | min/avg/max RTT, loss% | min/avg/max/mdev RTT, loss% |
| DNS 역방향 조회 | 미지원 | 지원 (`-n`으로 비활성화) |
| TTL 표시 | 미구현 | IP 헤더에서 TTL 추출 표시 |
| IPv6 | 미지원 | `ping6` 또는 `-6` 옵션 |

## 패킷 구조 비교

### 과제 구현 패킷

```
+------+------+----------+------+----------+-----------+
| Type | Code | Checksum |  ID  | Sequence | Timestamp |
|  8   |  0   |  2bytes  | PID  |  1..N    |  8 bytes  |
+------+------+----------+------+----------+-----------+
Total: 16 bytes (header 8 + payload 8)
```

### 시스템 ping 패킷

```
+------+------+----------+------+----------+----------+--------+
| Type | Code | Checksum |  ID  | Sequence | Timestamp| Padding|
|  8   |  0   |  2bytes  | PID  |  1..N    |  16 bytes| 40 B   |
+------+------+----------+------+----------+----------+--------+
Total: 64 bytes (header 8 + payload 56)
```

시스템 ping은 더 큰 payload를 사용하여 네트워크 경로의 MTU 문제를 감지하기 용이하다.

## RTT 측정 방식 비교

### 과제 구현

```python
# 전송 시 timestamp를 payload에 포함
payload = struct.pack("!d", time.time())

# 수신 시 payload에서 timestamp 추출
send_time = struct.unpack("!d", payload[:8])[0]
rtt_ms = (recv_time - send_time) * 1000
```

- `time.time()` — 마이크로초 정밀도 (부동소수점)
- 네트워크 바이트 순서(`!d`)로 패킹

### 시스템 ping

- `gettimeofday()` 또는 `clock_gettime(CLOCK_MONOTONIC)` 사용
- 단조 시계(monotonic clock) 사용으로 시스템 시간 변경에 영향 없음
- 나노초 정밀도

## `select()` vs 블로킹 `recvfrom()`

과제에서는 `select()`를 사용하여 타임아웃을 구현한다:

```python
ready, _, _ = select.select([raw_socket], [], [], timeout)
if ready:
    data, addr = raw_socket.recvfrom(1024)
```

**대안 — `settimeout()`**:
```python
raw_socket.settimeout(1.0)
try:
    data, addr = raw_socket.recvfrom(1024)
except socket.timeout:
    print("Request timed out")
```

| 방식 | 장점 | 단점 |
| :--- | :--- | :--- |
| `select()` | 정확한 잔여 시간 계산 가능 | 코드가 약간 복잡 |
| `settimeout()` | 간단한 코드 | 총 대기시간 정밀 제어 어려움 |

과제에서 `select()`를 선택한 이유: 시스템 ping 유틸리티와 동일한 방식이며, 타임아웃 시간을 정밀하게 제어할 수 있다.

## IP 헤더 처리

`recvfrom()`으로 수신한 데이터에는 IP 헤더가 포함되어 있다:

```python
# IP 헤더 길이 계산 (IHL 필드 × 4)
ip_header_len = (data[0] & 0x0F) * 4  # 보통 20바이트

# ICMP 데이터는 IP 헤더 이후
icmp_data = data[ip_header_len:]
```

**주의**: IP 헤더는 항상 20바이트가 아니다. 옵션 필드가 있으면 최대 60바이트까지 확장된다.
따라서 IHL(Internet Header Length) 필드를 읽어서 동적으로 계산해야 한다.

## 보안 고려사항

### Raw 소켓 권한

| OS | 방법 |
| :--- | :--- |
| Linux | `sudo` 또는 `CAP_NET_RAW` capability |
| macOS | `sudo` 필수 |
| Windows | 관리자 권한 |

### macOS 특수 소켓

macOS에서는 `SOCK_DGRAM`에 `IPPROTO_ICMP`를 조합한 "non-privileged ICMP socket"이 가능하다:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
```

이 방식은 root 권한 없이 ICMP를 사용할 수 있지만, IP 헤더가 포함되지 않아 TTL 정보를 얻을 수 없다.

## Ping Flood / DDoS 방지

ICMP는 rate limiting 없이 사용하면 네트워크 공격(Ping Flood, Smurf Attack)에 악용될 수 있다.
과제 구현에서는 각 ping 사이에 1초 간격을 두어 이를 방지한다:

```python
if seq < count:
    time.sleep(max(0, 1.0 - (time.time() - send_time)))
```

시스템 ping도 기본 1초 간격이며, `ping -f`(flood) 모드는 root만 사용할 수 있다.
