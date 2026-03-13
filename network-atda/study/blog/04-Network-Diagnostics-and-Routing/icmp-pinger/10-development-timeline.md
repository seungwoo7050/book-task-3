# ICMP Pinger development timeline

`ICMP Pinger`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `ICMP Pinger`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def internet_checksum`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: RFC 1071 인터넷 체크섬

핵심 코드/trace:

```python
def internet_checksum(data: bytes) -> int:
    """Internet checksum(RFC 1071)을 계산한다.

    Args:
        data: checksum을 계산할 bytes.

    Returns:
        16-bit checksum 값.
    """
    if len(data) % 2 != 0:
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem help
  run-client           Run the skeleton ICMP pinger (requires sudo)
  run-solution         Run the solution ICMP pinger (requires sudo)
  test                 Run deterministic ICMP tests without raw sockets
  test-live            Run the live raw-socket ICMP check (requires sudo)
```

## 2. checksum, packet build, reply parse를 ping 흐름으로 연결하기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `Raw socket으로 ICMP Echo Request/Reply를 직접 구현하는 진단 도구 과제입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def ping` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: raw socket 권한 모델

핵심 코드/trace:

```python
def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
    """ICMP Echo Request를 보내고 결과를 출력한다.

    Args:
        host: 대상 hostname 또는 IP address.
        count: 보낼 ping 횟수.
        timeout: 각 ping의 timeout 초.
    """
    # hostname을 IP로 해석한다.
    try:
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ rg -n -e 'def internet_checksum' -e 'def build_echo_request' -e 'def parse_echo_reply' -e 'def ping' 'study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py' 'study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py'
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:25:def internet_checksum(data: bytes) -> int:
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:49:def build_echo_request(identifier: int, sequence: int) -> bytes:
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:88:def parse_echo_reply(
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:125:def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
```

## 3. 테스트와 남은 범위를 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`를 다시 실행하고, `def test_ping_prints_successful_reply_and_loss_stats`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: IP header length(`IHL`) 파싱

핵심 코드/trace:

```python
def test_ping_prints_successful_reply_and_loss_stats(monkeypatch, capsys):
    fake_socket = FakeRawSocket({1})
    fake_clock = FakeClock(1000.0, 1000.0, 1000.05, 1000.10, 1001.0, 1001.0)

    monkeypatch.setattr(icmp_pinger.socket, "gethostbyname", lambda host: "203.0.113.10")
    monkeypatch.setattr(icmp_pinger.socket, "socket", lambda *args, **kwargs: fake_socket)
    monkeypatch.setattr(icmp_pinger.select, "select", _fake_select)
    monkeypatch.setattr(icmp_pinger.os, "getpid", lambda: 0x1234)
    monkeypatch.setattr(icmp_pinger.time, "time", fake_clock.time)
    monkeypatch.setattr(icmp_pinger.time, "sleep", fake_clock.sleep)
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
...........                                                              [100%]
11 passed in 0.01s
```

## 남은 경계

- IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
