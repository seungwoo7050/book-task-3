# Selective Repeat development timeline

`Selective Repeat`는 결과만 보면 단순해 보이지만, 실제로는 어느 파일에서 규칙을 고정했는지 따라가야 전체 그림이 보인다.

아래 순서는 README 설명을 다시 요약한 것이 아니라, 실제 근거가 남아 있는 지점을 따라 재조립한 흐름이다.

## 구현 순서 한눈에 보기

1. `study/02-Reliable-Transport/selective-repeat/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/02-Reliable-Transport/selective-repeat/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

출발점에서 중요한 건 기능 목록이 아니라 읽는 순서였다. `problem/` 문서와 Makefile만으로도 첫 발을 어디에 둘지 정리할 수 있었다.

- 당시 목표: `Selective Repeat`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def selective_repeat_send_receive`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: 패킷별 timer 관리

핵심 코드/trace:

```python
def selective_repeat_send_receive(
    channel_data: UnreliableChannel,
    channel_ack: UnreliableChannel,
    data_list: list[str],
    window_size: int = 4,
) -> list[str]:
    """단일 event loop 안에서 Selective Repeat로 메시지를 전송한다."""
    total = len(data_list)
    packets = [make_packet(i, item.encode()) for i, item in enumerate(data_list)]
    delivered: list[str] = []
```

왜 이 코드가 중요했는가:

첫 단계에서 이 코드를 붙드는 편이 좋은 이유는, 뒤 단계 전체가 여기서 정한 입력과 실행 방식 위에 쌓이기 때문이다.

CLI:

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem help
  run-skeleton         Run the Selective Repeat skeleton
  run-solution         Run the Selective Repeat solution
  test                 Run the automated Selective Repeat checks
```

## 2. window, 버퍼, timer를 Selective Repeat 규칙으로 묶기

두 번째 단계에서는 `Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.`라는 설명을 실제 코드나 trace 근거에 붙여야 했다. 그래서 파일 전체를 훑기보다 판단이 몰린 구간 하나를 먼저 골랐다.

- 당시 목표: `Go-Back-N의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.`를 실제 근거에 붙인다.
- 실제 진행: `recv_buffer` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: 수신 버퍼와 in-order delivery

핵심 코드/trace:

```python
recv_base = 0
    recv_buffer: dict[int, str] = {}

    while len(delivered) < total:
        while next_seq < min(send_base + window_size, total):
            print(f"[SENDER]   Sent packet seq={next_seq}: \"{data_list[next_seq]}\"")
            channel_data.send(packets[next_seq])
            timers[next_seq] = time.time()
            next_seq += 1

        if channel_data.has_packet():
```

왜 이 코드가 중요했는가:

이 스니펫은 실제 판단이 몰린 줄을 보여 준다. 설명을 길게 하기보다 이 줄을 기준으로 앞뒤 규칙을 읽는 편이 빠르다.

CLI:

```bash
$ rg -n -e 'def selective_repeat_send_receive' -e 'recv_buffer' -e 'Timeout! Retransmitting' -e 'def test_selective_repeat_delivers_all_messages_without_loss' 'study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py' 'study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py'
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:29:def selective_repeat_send_receive(
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:48:    recv_buffer: dict[int, str] = {}
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:62:                    if seq not in recv_buffer:
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:63:                        recv_buffer[seq] = payload.decode()
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:69:                    while recv_base in recv_buffer:
study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py:70:                        message = recv_buffer.pop(recv_base)
```

## 3. 테스트와 남은 범위를 정리하기

검증 단계에서는 결과보다 계약을 봤다. 어떤 출력이 통과 신호인지, 그리고 README에 남겨 둔 한계가 무엇인지 함께 정리했다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/02-Reliable-Transport/selective-repeat/problem test`를 다시 실행하고, `def test_selective_repeat_delivers_all_messages_without_loss`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: ACKed 집합과 sender base 업데이트

핵심 코드/trace:

```python
def test_selective_repeat_delivers_all_messages_without_loss():
    messages = ["A", "B", "C", "D"]
    delivered = selective_repeat_send_receive(
        UnreliableChannel(loss_rate=0.0, corrupt_rate=0.0),
        UnreliableChannel(loss_rate=0.0, corrupt_rate=0.0),
        messages,
        window_size=3,
    )
    assert delivered == messages
```

왜 이 코드가 중요했는가:

본문을 여기로 닫으면 구현 설명이 감상문으로 흘러가지 않는다. 어떤 계약을 확인했는지 바로 보이기 때문이다.

CLI:

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem test
TEST: Selective Repeat completes transfer      [PASS]
TEST: Sender retransmits selectively           [PASS]
 Results: 2 passed, 0 failed
```

## 남은 경계

- 실제 병렬 스레드 모델은 아닙니다.
- sequence wraparound는 구현하지 않았습니다.
- 성능 비교 표는 아직 정리하지 않았습니다.
