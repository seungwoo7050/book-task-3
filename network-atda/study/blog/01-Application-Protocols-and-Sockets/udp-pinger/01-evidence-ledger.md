# UDP Pinger evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `UDP Pinger`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/udp-pinger/problem/README.md`, `study/01-Application-Protocols-and-Sockets/udp-pinger/problem/Makefile`, `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`
- 무슨 판단을 했는가: 처음엔 코드를 바로 읽기보다, 공개 진입점과 성공 기준부터 고정하는 편이 안전하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem help
  run-server         Start the UDP ping server on port $(PORT)
  run-client         Run the skeleton ping client
  run-solution       Run the solution ping client
  test               Run the test script with a temporary UDP server
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 웹 서버 다음 단계에서 "연결이 없는 전송"이 애플리케이션 코드에 어떤 책임을 남기는지 분명하게 드러냅니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`의 `PING_COUNT = 10`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. 반복 ping, timeout, RTT 통계를 한 루프로 붙들기

- 당시 목표: `UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`
- 무슨 판단을 했는가: 핵심 설명은 한두 함수나 section에 가장 진하게 모여 있을 거라고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'PING_COUNT = 10' -e 'for seq in range' -e 'socket.timeout' -e 'loss_pct =' 'study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py' 'study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py'
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:15:PING_COUNT = 10
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:35:    for seq in range(1, PING_COUNT + 1):
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:54:        except socket.timeout:
study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py:61:    loss_pct = (lost / sent) * 100
study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py:29:        for seq in range(1, 11):
study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py:35:            except socket.timeout:
```
- 검증 신호:
  - 이 출력만으로도 `for seq in range(1, PING_COUNT + 1):` 주변이 설명의 중심축이라는 점이 드러난다.
  - 1초 timeout을 손실 판정으로 바꾸는 방법
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/udp-pinger/python/src/udp_pinger_client.py`의 `for seq in range(1, PING_COUNT + 1):`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 마지막에는 성공 신호와 한계를 같이 적어야 글이 매끈한 회고문으로 변하지 않는다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test
10 packets sent, 6 received, 40.0% loss
TEST: Output contains Ping lines               [PASS]
TEST: Output contains statistics               [PASS]
TEST: At least one RTT measurement             [PASS]
 Results: 3 passed, 0 failed
```
- 검증 신호:
  - `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - 패킷 순서 역전은 별도 처리하지 않습니다.
- 핵심 코드/trace 앵커: `study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests/test_udp_pinger.py`의 `def test_server_responds_to_ping`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
