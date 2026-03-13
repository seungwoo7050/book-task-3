# UDP Pinger 개발 타임라인

## Day 1

### Session 1

- 목표: Web Server 바로 뒤라 TCP 감각이 남아 있는 상태. UDP가 코드 수준에서 어디서부터 다른지를 skeleton과 제공 서버로 먼저 잡는다.
- 진행: `udp_pinger_server.py`를 열어 보니 `random.randint(0, 10) < 4`일 때 응답을 안 보내는 구조였다. 즉 서버가 30% 확률로 packet을 씹는다. Web Server에서는 서버 코드를 내가 짰는데, 이번에는 서버가 일부러 망가져 있고 클라이언트 쪽에서 버텨야 한다.
- 이슈: 당시 첫 의문은 "TCP에서는 `connect()`를 했는데 UDP는 왜 안 하지?"였다. `SOCK_DGRAM`은 연결이 없으니 `sendto()`에 주소를 매번 넘긴다는 걸 skeleton에서 보고 나서야 이해됐다.

```py
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

이 한 줄이 TCP와 전부 다르다. `listen()`, `accept()`, `connect()` 없이 바로 `sendto()`로 간다.

### Session 2

- 목표: timeout 없이 먼저 보내고 받아 본다.
- 진행: skeleton에 `sendto()` → `recvfrom()`을 넣고 서버를 띄운 뒤 돌려 봤다.
- 이슈: 서버가 packet을 버리는 순간 `recvfrom()`이 영원히 멈췄다. Ctrl+C를 누르기 전까지 프로그램이 돌아오질 않았다. TCP에서는 서버가 끊으면 `recv()`가 빈 문자열을 리턴했는데, UDP는 "모르겠고 기다린다"가 기본이었다.
- 판단: `settimeout()`을 반드시 걸어야 한다. 이게 없으면 손실을 감지할 방법 자체가 없다.

```py
client_socket.settimeout(TIMEOUT)  # 1초
```

이때부터 "UDP에서 timeout은 선택이 아니라 생존 조건"이라는 확신이 생겼다.

### Session 3

- 목표: 10번 루프와 RTT 측정, timeout 판정을 한 흐름으로 묶는다.
- 진행: `send_time = time.time()` → `sendto()` → `recvfrom()` → `recv_time = time.time()` → RTT 계산. `socket.timeout` 예외가 나면 그 ping은 "Request timed out"으로 기록.
- 이슈: 초기 버전에서 timeout이 났을 때 루프를 `break`해 버려서 10번을 다 못 돌았다. "응답이 없으면 끝"이 아니라 "응답이 없어도 다음 시도를 계속한다"가 이 과제의 핵심이었다.
- 조치: `except socket.timeout` 안에서 `continue`가 아니라 출력만 하고 루프를 자연스럽게 돌게 했다.

```py
try:
    client_socket.sendto(message.encode(), server_address)
    data, addr = client_socket.recvfrom(1024)
    rtt_ms = (recv_time - send_time) * 1000
    rtt_list.append(rtt_ms)
    print(f"Ping {seq:2d}: Reply from {addr[0]}  RTT = {rtt_ms:.3f} ms")
except socket.timeout:
    print(f"Ping {seq:2d}: Request timed out")
```

이 구조가 만들어지니 성공/실패에 관계없이 10번을 반드시 완주하는 클라이언트가 됐다.

### Session 4

- 목표: 통계 요약까지 마무리하고 `make test`를 돌린다.
- 진행:

```py
sent = PING_COUNT
received = len(rtt_list)
lost = sent - received
loss_pct = (lost / sent) * 100
```

- 이슈: `rtt_list`가 비어 있으면(100% loss) `min(rtt_list)`에서 `ValueError`가 난다. 별도 분기를 넣어야 했다.
- 검증:

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test
Starting UDP Pinger Server on port 12000...
Running UDP Pinger Client...
Ping  1: Reply from 127.0.0.1  RTT = 0.284 ms
Ping  2: Request timed out
Ping  3: Reply from 127.0.0.1  RTT = 0.198 ms
Ping  4: Reply from 127.0.0.1  RTT = 0.312 ms
Ping  5: Request timed out
Ping  6: Reply from 127.0.0.1  RTT = 0.156 ms
Ping  7: Reply from 127.0.0.1  RTT = 0.247 ms
Ping  8: Request timed out
Ping  9: Reply from 127.0.0.1  RTT = 0.189 ms
Ping 10: Reply from 127.0.0.1  RTT = 0.221 ms
--- Ping Statistics ---
10 packets sent, 7 received, 30.0% loss
RTT min/avg/max = 0.156/0.230/0.312 ms
All tests passed!
```

- 정리:
  - 이 프로젝트에서 가장 중요한 한 줄은 `settimeout(1)`이었다. 이게 없으면 나머지 코드가 전부 무의미하다.
  - TCP에서는 "연결 → 전송 → 종료"라는 구조가 보장됐지만, UDP에서는 "보냈지만 돌아올지 모른다"를 코드로 직접 처리해야 했다.
  - 통계 계산은 최종 출력용으로만 보였지만, 실제로는 이 요약부가 UDP 특성을 학습 결과로 묶는 결정적인 지점이었다.
  - 다음은 SMTP — TCP 위의 또 다른 프로토콜이지만, HTTP와 달리 상태 전이가 더 길다.
