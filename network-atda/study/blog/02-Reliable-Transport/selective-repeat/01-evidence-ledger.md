# Selective Repeat evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `Selective Repeat`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/02-Reliable-Transport/selective-repeat/problem/README.md`, `study/02-Reliable-Transport/selective-repeat/problem/Makefile`, `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`
- 무슨 판단을 했는가: 어디서 실행하고 어디서 검증하는지 먼저 정하지 않으면 본문이 기능 요약으로 흘러갈 가능성이 컸다.
- 실행한 CLI:

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem help
  run-skeleton         Run the Selective Repeat skeleton
  run-solution         Run the Selective Repeat solution
  test                 Run the automated Selective Repeat checks
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 교재 흐름상 당연히 이어져야 할 Selective Repeat를 별도 프로젝트로 분리해, 재전송 정책과 수신 버퍼링의 차이를 코드 수준에서 비교할 수 있게 합니다.
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`의 `def selective_repeat_send_receive`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. window, 버퍼, timer를 Selective Repeat 규칙으로 묶기

- 당시 목표: `Go-Back-N의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`
- 무슨 판단을 했는가: 전체 파일을 다 설명하기보다, 판단이 바뀐 줄 몇 개를 먼저 붙드는 편이 더 정확하다고 판단했다.
- 실행한 CLI:

```bash
$ rg -n -e 'def selective_repeat_send_receive' -e 'recv_buffer' -e 'Timeout! Retransmitting' -e 'def test_selective_repeat_delivers_all_messages_without_loss' 'study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py' 'study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py'
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:29:def selective_repeat_send_receive(
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:48:    recv_buffer: dict[int, str] = {}
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:62:                    if seq not in recv_buffer:
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:63:                        recv_buffer[seq] = payload.decode()
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:69:                    while recv_base in recv_buffer:
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:70:                        message = recv_buffer.pop(recv_base)
```
- 검증 신호:
  - 이 출력만으로도 `recv_buffer` 주변이 설명의 중심축이라는 점이 드러난다.
  - 수신 버퍼와 in-order delivery
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`의 `recv_buffer`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 테스트 통과만 적으면 과장이 되기 쉬워서, 어디까지 확인됐고 무엇이 남는지도 같이 적어야 한다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem test
TEST: Selective Repeat completes transfer      [PASS]
TEST: Sender retransmits selectively           [PASS]
 Results: 2 passed, 0 failed
```
- 검증 신호:
  - `make -C study/02-Reliable-Transport/selective-repeat/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - 실제 병렬 스레드 모델은 아닙니다.
- 핵심 코드/trace 앵커: `study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`의 `def test_selective_repeat_delivers_all_messages_without_loss`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
