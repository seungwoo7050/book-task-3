# UDP Pinger development timeline

`UDP Pinger`의 핵심은 완성 결과보다, 어떤 순서로 범위를 좁히고 검증까지 닫았는가에 있다.

본문은 코드나 trace를 한 번에 길게 복붙하지 않고, 판단이 바뀐 지점만 골라 이어 붙인다.

## 구현 순서 한눈에 보기

1. `study/01-Application-Protocols-and-Sockets/udp-pinger/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

처음에는 `UDP Pinger`를 어디서부터 설명해야 할지부터 정리해야 했다. 그래서 문제 문서와 `make help` 출력으로 공개된 실행 표면을 먼저 잡았다.

- 당시 목표: `UDP Pinger`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `PING_COUNT = 10`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: UDP의 connectionless socket 사용법

핵심 코드/trace:

```python
PING_COUNT = 10
TIMEOUT = 1  # 초


def main(host: str = "127.0.0.1", port: int = 12000) -> None:
    """ping을 보내고 RTT 통계를 수집한다.

    Args:
        host: server hostname 또는 IP address.
        port: server UDP port 번호.
```

왜 이 코드가 중요했는가:

이 부분을 먼저 보여 주는 이유는, 이 프로젝트의 진입점과 실행 표면이 여기서 한 번에 정리되기 때문이다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem help
  run-server         Start the UDP ping server on port $(PORT)
  run-client         Run the skeleton ping client
  run-solution       Run the solution ping client
  test               Run the test script with a temporary UDP server
```

## 2. 반복 ping, timeout, RTT 통계를 한 루프로 붙들기

이제부터는 설명을 추상적으로 유지할 수 없었다. 실제 분기나 frame evidence가 모이는 지점을 찾아야 글이 살아났다.

- 당시 목표: `UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.`를 실제 근거에 붙인다.
- 실제 진행: `for seq in range(1, PING_COUNT + 1):` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: 1초 timeout을 손실 판정으로 바꾸는 방법

핵심 코드/trace:

```python
for seq in range(1, PING_COUNT + 1):
        # sequence 번호와 timestamp를 포함한 ping 메시지를 만든다.
        send_time = time.time()
        message = f"Ping {seq} {send_time}"

        try:
            # ping datagram을 전송한다.
            client_socket.sendto(message.encode(), server_address)

            # 응답을 기다린다.
```

왜 이 코드가 중요했는가:

여기서는 구현이나 분석의 무게중심이 바뀐다. 그래서 파일 전체보다 이 좁은 구간을 먼저 보는 편이 훨씬 정확하다.

CLI:

```bash
$ rg -n -e 'PING_COUNT = 10' -e 'for seq in range' -e 'socket.timeout' -e 'loss_pct =' 'study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py' 'study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py'
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:15:PING_COUNT = 10
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:35:    for seq in range(1, PING_COUNT + 1):
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:54:        except socket.timeout:
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:61:    loss_pct = (lost / sent) * 100
study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py:29:        for seq in range(1, 11):
study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py:35:            except socket.timeout:
```

## 3. 테스트와 남은 범위를 정리하기

끝맺음에서 중요한 건 멋진 회고가 아니라 경계선이다. 통과한 범위와 남겨 둔 범위를 같은 문맥 안에 두려고 했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`를 다시 실행하고, `def test_server_responds_to_ping`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: RTT 최소값/평균값/최대값과 손실률 계산

핵심 코드/trace:

```python
def test_server_responds_to_ping(self):
        """server는 여러 ping 중 일부에는 응답해야 한다."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        replies = 0

        for seq in range(1, 11):
            msg = f"Ping {seq} {time.time()}"
            sock.sendto(msg.encode(), (HOST, PORT))
            try:
```

왜 이 코드가 중요했는가:

최종 단계에서 중요한 것은 '잘 됐다'가 아니라 '무엇을 확인했고 무엇은 아직 안 했다'인데, 그 기준이 이 파일에 가장 잘 남아 있다.

CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test
10 packets sent, 6 received, 40.0% loss
TEST: Output contains Ping lines               [PASS]
TEST: Output contains statistics               [PASS]
TEST: At least one RTT measurement             [PASS]
 Results: 3 passed, 0 failed
```

## 남은 경계

- 패킷 순서 역전은 별도 처리하지 않습니다.
- 분위수 같은 고급 통계는 계산하지 않습니다.
- `pytest` 단독 실행은 제공 서버 선기동이 필요합니다.
