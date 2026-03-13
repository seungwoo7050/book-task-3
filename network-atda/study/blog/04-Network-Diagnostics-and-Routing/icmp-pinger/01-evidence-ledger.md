# ICMP Pinger evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `ICMP Pinger`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/README.md`, `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/Makefile`, `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem help
  run-client           Run the skeleton ICMP pinger (requires sudo)
  run-solution         Run the solution ICMP pinger (requires sudo)
  test                 Run deterministic ICMP tests without raw sockets
  test-live            Run the live raw-socket ICMP check (requires sudo)
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 응용 계층 소켓 과제보다 한 단계 아래로 내려가 IP/ICMP 레벨에서 무엇이 직접 보이는지 체감하게 합니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`의 `def internet_checksum`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. checksum, packet build, reply parse를 ping 흐름으로 연결하기

- 당시 목표: `Raw socket으로 ICMP Echo Request/Reply를 직접 구현하는 진단 도구 과제입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'def internet_checksum' -e 'def build_echo_request' -e 'def parse_echo_reply' -e 'def ping' 'study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py' 'study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py'
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:25:def internet_checksum(data: bytes) -> int:
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:49:def build_echo_request(identifier: int, sequence: int) -> bytes:
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:88:def parse_echo_reply(
study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py:125:def ping(host: str, count: int = 4, timeout: float = 1.0) -> None:
```
- 검증 신호:
  - 이 출력만으로도 `def ping` 주변이 설명의 중심축이라는 점이 드러난다.
  - raw socket 권한 모델
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`의 `def ping`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
...........                                                              [100%]
11 passed in 0.01s
```
- 검증 신호:
  - `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - IPv6/ICMPv6는 지원하지 않습니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`의 `def test_ping_prints_successful_reply_and_loss_stats`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
