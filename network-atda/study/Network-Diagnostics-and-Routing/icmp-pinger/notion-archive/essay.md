# ICMP Pinger — 네트워크 레이어에서 패킷을 직접 만들다

## 응용 계층 아래로 내려간 순간

지금까지의 과제(웹 서버, UDP 핑, SMTP 클라이언트, 웹 프록시)는 전부 **응용 계층**에서 동작했다. TCP든 UDP든 소켓을 열면 OS가 IP 헤더, TCP/UDP 헤더를 알아서 붙여줬다. 우리는 페이로드만 신경쓰면 됐다.

ICMP 핑은 다르다. ICMP는 응용 계층 프로토콜이 아니라 **네트워크 레이어 프로토콜**이다. TCP/UDP 포트 개념이 없다. OS의 TCP/UDP 스택을 거치지 않고, **raw socket**을 열어 ICMP 패킷을 직접 바이트로 조립해서 보내야 한다.

이 과제를 만든 첫 번째 새로운 경험은 `sudo`가 필요하다는 것이었다.

```bash
sudo python3 icmp_pinger.py google.com
```

일반 사용자 권한으로 raw socket을 열면 `PermissionError`가 난다. 이건 보안 이유다 — raw socket은 네트워크 패킷을 임의로 조작할 수 있어서, root 또는 `CAP_NET_RAW` 권한이 필요하다.

## ICMP 패킷의 구조: 직접 조립하기

ICMP Echo Request 패킷은 이렇게 생겼다:

```
+--------+--------+--------+--------+
|  Type  |  Code  |    Checksum     |
+--------+--------+--------+--------+
|     Identifier  | Sequence Number |
+--------+--------+--------+--------+
|            Payload (optional)     |
+--------+--------+--------+--------+
```

- **Type**: 8 (Echo Request) 또는 0 (Echo Reply)
- **Code**: 0
- **Checksum**: 패킷 전체의 인터넷 체크섬
- **Identifier**: 이 ping의 주인을 구분하는 ID (보통 PID)
- **Sequence Number**: 몇 번째 ping인지

이걸 `struct.pack()`으로 직접 바이트로 만든다:

```python
header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, identifier, sequence)
payload = struct.pack("!d", time.time())  # timestamp를 8바이트 double로
```

체크섬을 계산할 때 주의점이 있었다. **체크섬 필드를 0으로 놓고** 전체 패킷의 체크섬을 계산한 다음, 그 값을 다시 채워넣어야 한다. 체크섬 안에 체크섬 자체가 들어가면 안 되니까.

## 인터넷 체크섬: RFC 1071

이 체크섬 알고리즘은 간단하면서도 독특했다:

1. 패킷을 2바이트(16비트) 단위로 잘라서 전부 더한다
2. 캐리(overflow)가 나면 다시 하위 16비트에 더한다 (fold)
3. 결과를 비트 반전(~)한다

```python
def internet_checksum(data: bytes) -> int:
    if len(data) % 2 != 0:
        data += b"\x00"  # 홀수 길이면 패딩
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF
```

"왜 이렇게 복잡한 방식을 쓸까?"라고 생각했는데, 이 알고리즘의 장점은 **바이트 순서(endianness)에 독립적**이라는 것이다. 빅엔디안이든 리틀엔디안이든 같은 결과가 나온다. 1980년대에 다양한 하드웨어에서 동작해야 했던 프로토콜이 이 방식을 선택한 이유가 이해됐다.

## 응답 파싱: IP 헤더를 벗겨내야 한다

`recvfrom()`으로 받은 데이터에는 운영체제가 붙인 **IP 헤더**가 포함되어 있다. ICMP 데이터를 읽으려면 IP 헤더의 길이(IHL)를 먼저 파악하고 건너뛰어야 한다:

```python
ip_header_len = (data[0] & 0x0F) * 4  # IHL 필드 × 4바이트
icmp_data = data[ip_header_len:]
```

IP 헤더의 첫 바이트 하위 4비트가 IHL(Internet Header Length)이다. 옵션이 없는 표준 IP 헤더는 20바이트(IHL=5)이지만, 옵션이 있으면 더 길어질 수 있다. 그래서 20을 하드코딩하지 않고 IHL을 동적으로 읽는 것이 정확한 구현이다.

## select.select()로 타임아웃 정밀 제어

UDP 핑에서는 `settimeout()`을 썼지만, ICMP 핑에서는 `select.select()`를 사용했다:

```python
ready, _, _ = select.select([raw_socket], [], [], timeout)
```

이유는 두 가지다:
1. `select`는 여러 소켓을 동시에 감시할 수 있다 (이 과제에서는 하나지만)
2. 타임아웃 후에도 소켓 상태를 깔끔하게 유지한다

`select`가 빈 리스트를 반환하면 타임아웃이다. 리스트에 소켓이 있으면 데이터가 도착한 것.

## Identifier로 내 패킷 구분하기

같은 시스템에서 여러 ping 프로그램이 동시에 돌 수 있다. raw socket으로 ICMP 응답을 받으면, 내가 보낸 요청의 응답인지 다른 프로세스 것인지 구분해야 한다.

이걸 위해 `identifier` 필드에 PID를 넣었다:

```python
identifier = os.getpid() & 0xFFFF  # PID의 하위 16비트
```

응답을 파싱할 때 이 identifier가 일치하는 패킷만 처리한다.

## 테스트: root 없이 검증하기

raw socket은 root 권한이 필요하다. CI 환경이나 일반 개발 환경에서는 root로 테스트를 돌리기 어렵다.

그래서 테스트를 두 계층으로 나눴다:

1. **deterministic test** (`make test`): root 불필요. 체크섬 계산, 패킷 빌드/파싱을 fake 데이터로 검증
2. **live test** (`sudo make test-live HOST=google.com`): root 필요. 실제 네트워크로 ping 보내서 응답 확인

대부분의 로직(체크섬, 패킷 조립, 응답 파싱, 통계 계산)은 deterministic test로 커버된다. 실제 네트워크 동작은 수동 검증 경로로 남겼다.

```bash
# root 없이 돌아가는 테스트
make -C problem test

# root 필요한 live 테스트
sudo make -C problem test-live HOST=google.com
```

## 이 과제에서 가져간 것

`struct.pack()`으로 바이너리 패킷을 직접 만들고, `struct.unpack()`으로 바이트를 해석하는 경험은 이후의 모든 네트워크 과제에서 반복됐다. 특히 UDP 바이너리 프로토콜(게임 서버의 InputPacket, SnapshotPacket)을 설계할 때, ICMP 패킷 구조를 다뤄본 경험이 직접적으로 적용됐다.

또한 "프로토콜 스택의 레이어를 직접 넘나드는" 경험이었다. 응용 계층에서 `socket.send()`를 호출하면 OS가 알아서 IP와 TCP/UDP를 붙여주지만, raw socket에서는 직접 ICMP 헤더를 만들고, 수신 데이터에서 IP 헤더를 파싱해서 제거해야 한다. 이 경험이 네트워크 스택의 계층 구조를 머릿속에 확실히 각인시켜줬다.

---

> **학습 키워드**: ICMP Echo Request/Reply, raw socket, `SOCK_RAW`, `struct.pack()`/`unpack()`, RFC 1071 인터넷 체크섬, IHL 파싱, `select.select()`, root 권한, 계층 분리 테스트