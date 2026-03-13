# Traceroute evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `Traceroute`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/traceroute/problem/README.md`, `study/04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile`, `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`
- 무슨 판단을 했는가: 어디서 실행하고 어디서 검증하는지 먼저 정하지 않으면 본문이 기능 요약으로 흘러갈 가능성이 컸다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem help
  run-client         Run the live traceroute implementation (requires sudo on most systems)
  test               Run parser, formatting, and synthetic route integration tests
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: `ICMP Pinger`와 `routing` 사이에서, 패킷 수준 TTL 개념이 실제 경로 탐색 도구로 어떻게 이어지는지 분명하게 보여 줍니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`의 `class ProbeObservation`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. probe port 계산, ICMP 파싱, hop formatting을 한 경로로 묶기

- 당시 목표: `TTL 증가와 ICMP Time Exceeded를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`
- 무슨 판단을 했는가: 전체 파일을 다 설명하기보다, 판단이 바뀐 줄 몇 개를 먼저 붙드는 편이 더 정확하다고 판단했다.
- 실행한 CLI:

```bash
$ rg -n -e 'def build_probe_port' -e 'def parse_icmp_response' -e 'def format_hop_line' -e 'def trace_route' 'study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py' 'study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py'
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:30:def build_probe_port(ttl: int, probe_index: int, probes_per_hop: int, base_port: int = DEFAULT_BASE_PORT) -> int:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:35:def parse_icmp_response(packet: bytes) -> tuple[int, int, int | None] | None:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:60:def format_hop_line(ttl: int, observations: list[ProbeObservation]) -> str:
study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py:84:def trace_route(
```
- 검증 신호:
  - 이 출력만으로도 `def trace_route` 주변이 설명의 중심축이라는 점이 드러난다.
  - embedded UDP port를 이용한 probe 매칭
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`의 `def trace_route`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 테스트 통과만 적으면 과장이 되기 쉬워서, 어디까지 확인됐고 무엇이 남는지도 같이 적어야 한다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test
....                                                                     [100%]
4 passed in 0.01s
```
- 검증 신호:
  - `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - IPv6 traceroute는 지원하지 않습니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`의 `def test_trace_route_returns_hops_until_destination`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
