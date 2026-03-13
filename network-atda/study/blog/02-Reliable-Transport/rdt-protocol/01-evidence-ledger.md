# RDT Protocol evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `RDT Protocol`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/02-Reliable-Transport/rdt-protocol/problem/README.md`, `study/02-Reliable-Transport/rdt-protocol/problem/Makefile`, `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`
- 무슨 판단을 했는가: 어디서 실행하고 어디서 검증하는지 먼저 정하지 않으면 본문이 기능 요약으로 흘러갈 가능성이 컸다.
- 실행한 CLI:

```bash
$ make -C study/02-Reliable-Transport/rdt-protocol/problem help
  run-gbn                  Run the GBN skeleton
  run-solution-gbn         Run the GBN solution
  test                     Run all tests
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 전송 계층 메커니즘을 가장 직접적으로 체험하는 중심 과제로, 이후 `Selective Repeat`를 비교할 때 기준점 역할을 합니다.
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`의 `def rdt_send_receive`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. 패킷 생성 규칙과 전송 루프를 비교 가능한 단위로 붙들기

- 당시 목표: `rdt3.0과 Go-Back-N을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`
- 무슨 판단을 했는가: 전체 파일을 다 설명하기보다, 판단이 바뀐 줄 몇 개를 먼저 붙드는 편이 더 정확하다고 판단했다.
- 실행한 CLI:

```bash
$ rg -n -e 'def rdt_send_receive' -e 'def gbn_send_receive' -e 'class TestPacketModule' -e 'def test_make_and_parse_packet' 'study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py' 'study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py' 'study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py'
study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py:28:def rdt_send_receive(
study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py:27:def gbn_send_receive(
study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py:16:class TestPacketModule:
study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py:19:    def test_make_and_parse_packet(self):
```
- 검증 신호:
  - 이 출력만으로도 `def gbn_send_receive` 주변이 설명의 중심축이라는 점이 드러난다.
  - timeout 기반 재전송
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`의 `def gbn_send_receive`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 테스트 통과만 적으면 과장이 되기 쉬워서, 어디까지 확인됐고 무엇이 남는지도 같이 적어야 한다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/02-Reliable-Transport/rdt-protocol/problem test
TEST: RDT 3.0 completes transfer               [PASS]
TEST: GBN completes transfer                   [PASS]
 Results: 2 passed, 0 failed
```
- 검증 신호:
  - `make -C study/02-Reliable-Transport/rdt-protocol/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`의 `def test_make_and_parse_packet`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
