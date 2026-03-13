# Traceroute development timeline

`Traceroute`는 결과만 보면 단순해 보이지만, 실제로는 어느 파일에서 규칙을 고정했는지 따라가야 전체 그림이 보인다.

아래 순서는 README 설명을 다시 요약한 것이 아니라, 실제 근거가 남아 있는 지점을 따라 재조립한 흐름이다.

## 구현 순서 한눈에 보기

1. `study/04-Network-Diagnostics-and-Routing/traceroute/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

출발점에서 중요한 건 기능 목록이 아니라 읽는 순서였다. `problem/` 문서와 Makefile만으로도 첫 발을 어디에 둘지 정리할 수 있었다.

- 당시 목표: `Traceroute`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `class ProbeObservation`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: TTL과 `ICMP Time Exceeded`의 연결

핵심 코드/trace:

```python
@dataclass
class ProbeObservation:
    responder: str | None
    rtt_ms: float | None
    icmp_type: int | None
    icmp_code: int | None


def build_probe_port(ttl: int, probe_index: int, probes_per_hop: int, base_port: int = DEFAULT_BASE_PORT) -> int:
    """probe마다 안정적인 UDP destination port를 계산한다."""
    return base_port + (ttl - 1) * probes_per_hop + probe_index
```

왜 이 코드가 중요했는가:

첫 단계에서 이 코드를 붙드는 편이 좋은 이유는, 뒤 단계 전체가 여기서 정한 입력과 실행 방식 위에 쌓이기 때문이다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem help
  run-client         Run the live traceroute implementation (requires sudo on most systems)
  test               Run parser, formatting, and synthetic route integration tests
```

## 2. probe port 계산, ICMP 파싱, hop formatting을 한 경로로 묶기

두 번째 단계에서는 `TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.`라는 설명을 실제 코드나 trace 근거에 붙여야 했다. 그래서 파일 전체를 훑기보다 판단이 몰린 구간 하나를 먼저 골랐다.

- 당시 목표: `TTL 증가와 ICMP Time Exceeded를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def trace_route` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: embedded UDP port를 이용한 probe 매칭

핵심 코드/trace:

```python
def trace_route(
    host: str,
    max_hops: int = 30,
    probes_per_hop: int = 3,
    timeout: float = 1.0,
    base_port: int = DEFAULT_BASE_PORT,
) -> list[str]:
    """경로를 추적하고 출력용 hop line 목록을 반환한다."""
    destination_ip = resolve_target(host)
    lines = [f"traceroute to {host} ({destination_ip}), {max_hops} hops max"]
```

왜 이 코드가 중요했는가:

이 스니펫은 실제 판단이 몰린 줄을 보여 준다. 설명을 길게 하기보다 이 줄을 기준으로 앞뒤 규칙을 읽는 편이 빠르다.

CLI:

```bash
$ rg -n -e 'def build_probe_port' -e 'def parse_icmp_response' -e 'def format_hop_line' -e 'def trace_route' 'study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py' 'study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py'
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:30:def build_probe_port(ttl: int, probe_index: int, probes_per_hop: int, base_port: int = DEFAULT_BASE_PORT) -> int:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:35:def parse_icmp_response(packet: bytes) -> tuple[int, int, int | None] | None:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:60:def format_hop_line(ttl: int, observations: list[ProbeObservation]) -> str:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:84:def trace_route(
```

## 3. 테스트와 남은 범위를 정리하기

검증 단계에서는 결과보다 계약을 봤다. 어떤 출력이 통과 신호인지, 그리고 README에 남겨 둔 한계가 무엇인지 함께 정리했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`를 다시 실행하고, `def test_trace_route_returns_hops_until_destination`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: live probing과 synthetic integration test 분리

핵심 코드/trace:

```python
def test_trace_route_returns_hops_until_destination(monkeypatch):
    route_map = {
        1: ("10.0.0.1", 11, 0),
        2: ("10.0.1.1", 11, 0),
        3: ("203.0.113.9", 3, 3),
    }
    recv_socket = FakeRecvSocket(route_map)
    fake_clock = FakeClock()

    def fake_socket_factory(_family, sock_type, protocol):
```

왜 이 코드가 중요했는가:

본문을 여기로 닫으면 구현 설명이 감상문으로 흘러가지 않는다. 어떤 계약을 확인했는지 바로 보이기 때문이다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test
....                                                                     [100%]
4 passed in 0.01s
```

## 남은 경계

- IPv6 traceroute는 지원하지 않습니다.
- DNS reverse lookup은 포함하지 않습니다.
- ECMP나 비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않습니다.
