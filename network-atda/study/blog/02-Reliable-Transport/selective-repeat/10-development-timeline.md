# Selective Repeat 개발 타임라인

## Day 1

### Session 1

- 목표: GBN의 로그에서 봤던 "청소년 비효율" — seq 2만 죽었는데 3, 4도 다시 보내는 문제를 어떻게 고치는지 코드로 확인한다.
- 진행: GBN과 SR의 차이를 먼저 두 가지로 정리했다.
  1. **receiver**: GBN은 out-of-order를 버리지만, SR은 window 안이면 buffer에 넣는다.
  2. **sender**: GBN은 단일 timer로 window 전체를 재전송하지만, SR은 packet별 timer로 해당 packet만 재전송한다.
- 이슈: 당시에는 "receiver에 buffer를 넣는 게 그렇게 복잡한가?"라고 생각했다. 막상 코드를 쓰니 buffer insert는 간단했지만, `recv_base`를 언제 앞으로 미는지가 진짜 문제였다.

```py
if recv_base <= seq < recv_base + window_size:
    if seq not in recv_buffer:
        recv_buffer[seq] = payload.decode()
    channel_ack.send(make_ack(seq))

    while recv_base in recv_buffer:
        delivered.append(recv_buffer.pop(recv_base))
        recv_base += 1
```

`recv_base`는 buffer에 연속적으로 채워진 부분이 있을 때만 앞으로 간다. seq 0, 2, 3이 buffer에 있어도 1이 없으면 0만 deliver하고 멈춘다. 이 `while recv_base in recv_buffer` 루프가 SR receiver의 핵심이었다.

### Session 2

- 목표: sender 측 per-packet timer를 구현한다.
- 진행: GBN의 timer는 `timer_start` 하나였지만, SR은 `timers: dict[int, float]` — seq마다 개별 시간을 기록한다.

```py
for seq in range(send_base, next_seq):
    if seq in acked:
        continue
    started = timers.get(seq)
    if started is not None and now - started > TIMEOUT:
        print(f"[SENDER]   Timeout! Retransmitting seq={seq}")
        channel_data.send(packets[seq])
        timers[seq] = time.time()
```

- 이슈: 처음에 이 루프를 GBN과 비교했을 때 "복잡도가 다를 게 없지 않나?"라고 느꼈다. 하지만 loss rate 20%에서 돌려 보니까 GBN은 5개 packet을 다 다시 보내는 반면, SR은 1개만 다시 보냈다. 코드 복잡도는 비슷해도 네트워크 효율은 명확히 달랐다.

### Session 3

- 목표: `send_base` slide 로직을 완성하고 전체를 검증한다.
- 진행: sender의 `acked` set에 ACK된 seq를 넣고, `send_base`부터 연속 ACK가 이어지는 만큼만 window를 밀었다.

```py
acked.add(ack_seq)
timers.pop(ack_seq, None)
while send_base in acked:
    acked.remove(send_base)
    send_base += 1
```

- 이슈: 처음에는 ACK이 오는 즉시 `send_base`를 올렸더니 중간 hole이 있을 때 window가 툭 뛰어버렸다. `while send_base in acked` 패턴을 잘아야 receiver의 `while recv_base in recv_buffer`와 대칭이 맞았다.
- 검증:

CLI:

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem run-solution
=== Selective Repeat (Window Size = 4) ===
[SENDER]   Sent packet seq=0: "Hello"
[SENDER]   Sent packet seq=1: "World"
[SENDER]   Sent packet seq=2: "RDT"
[SENDER]   Sent packet seq=3: "Protocol"
[RECEIVER] Buffered seq=0 → ACK 0
[RECEIVER] Delivered seq=0: "Hello"
[RECEIVER] Buffered seq=2 → ACK 2
[SENDER]   ACK 0 received
[SENDER]   Timeout! Retransmitting seq=1
[RECEIVER] Buffered seq=1 → ACK 1
[RECEIVER] Delivered seq=1: "World"
[RECEIVER] Delivered seq=2: "RDT"
...
Status:   SUCCESS
```

```bash
$ make -C study/02-Reliable-Transport/selective-repeat/problem test
===== 3 passed =====
```

- 정리:
  - GBN 로그에서 "왜 seq 3, 4를 다시 보내지?" 하던 의문의 답이 SR의 receiver buffer + per-packet timer였다.
  - sender와 receiver 양쪽의 window slide가 대칭 구조라는 점이 코드로 보니 분명했다.
  - rdt3.0 → GBN → SR이라는 흐름이 "비효율을 느끼고 → 그 비효율의 원인을 정확히 고치는" 과정이었다.
  - 다음 트랙은 Packet Analysis — 구현이 아니라 실제 패킷을 읽는 쪽으로 넘어간다.
