# RDT Protocol 개발 타임라인

## Day 1 — rdt3.0 (Stop-and-Wait)

### Session 1

- 목표: 불신 채널 위의 전송을 교과서의 상태 다이어그램 대신 실제 코드로 읽어본다.
- 진행: 먼저 `channel.py`와 `packet.py`를 열었다. `UnreliableChannel`은 `send()` 시 loss/corruption을 확률적으로 적용하고, `packet.py`는 `make_packet()`, `parse_packet()`, `is_corrupt()`, `make_ack()`, `is_ack()`를 제공한다. 즉 패킷 조립과 검증은 제공되고, sender/receiver 상태 전이만 내가 짜야 한다.
- 이슈: 당시 가장 헷갈렸던 건 "번호가 0과 1만 있는데 어떻게 여러 packet을 순서대로 보내지?"였다. alternating bit이라는 이름은 알았지만, 실제로 0→1→0 전환만으로 5개, 10개 메시지를 순서대로 보낼 수 있는 이유를 코드로 보기 전에는 확신이 없었다.

### Session 2

- 목표: sender 상태 변수를 고정하고 stop-and-wait 루프를 돌린다.
- 진행: sender에 필요한 상태는 세 개였다 — `send_seq`(0 또는 1), `current_pkt`(재전송용 복사본), `timer_start`(timeout 판정용).

```py
current_pkt = make_packet(send_seq, data_list[send_idx].encode())
channel_data.send(current_pkt)
timer_start = time.time()
awaiting_ack = True
```

- 이슈: 처음에 `current_pkt`을 저장하지 않고 timeout 시 새로 `make_packet()`을 불렀더니, checksum이 달라져서 receiver가 corrupt로 판정하는 문제가 생겼다. 실제로 재전송은 "packet을 다시 만드는 게 아니라 똑같은 packet을 다시 보내는 것"이었다.
- 조치: `current_pkt`을 전송 전에 저장해 두고, timeout 시 그대로 다시 보내도록 수정.

### Session 3

- 목표: receiver 비정상 경로를 완성한다 — duplicate, corrupt.
- 진행: receiver는 `expected_seq`와 일치하면 deliver + ACK, 다르면 직전 ACK 재전송.

```py
if seq == expected_seq:
    received.append(msg)
    channel_ack.send(make_ack(expected_seq))
    expected_seq = 1 - expected_seq
else:
    prev = 1 - expected_seq
    channel_ack.send(make_ack(prev))
```

- 이슈: corrupt packet에 대해 처음에는 아무 응답도 안 보냈다. 그러니 sender가 timeout만 기다리게 됐는데, 이러면 채널이 좋을 때도 항상 timeout이 날 수 있었다. corrupt에도 직전 ACK를 보내는 편이 timeout 안에 sender가 구제됐다.
- 검증:

CLI:

```bash
$ make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-rdt3
=== RDT 3.0 (Stop-and-Wait) ===
Messages to send: 5
Loss rate: 0.2, Corruption rate: 0.1

[SENDER]   Sent packet seq=0: "Hello"
[RECEIVER] Received seq=0: "Hello" → ACK 0
[SENDER]   ACK 0 received
[SENDER]   Sent packet seq=1: "World"
[SENDER]   Timeout! Retransmitting seq=1
[RECEIVER] Received seq=1: "World" → ACK 1
[SENDER]   ACK 1 received
...
=== Transfer Complete ===
Sent:     5 messages
Received: 5 messages
Status:   SUCCESS — All messages delivered correctly!
```

## Day 2 — Go-Back-N

### Session 1

- 목표: rdt3.0의 stop-and-wait가 느린 이유를 코드로 느낀 뒤 sliding window를 넣는다.
- 진행: sender 상태가 `send_seq`(0 or 1) 대신 `base`, `next_seq`, `window_size` 세 개로 늘어났다. packet을 미리 다 만들어 두고, window 안에서 `next_seq`까지 연속 전송한다.
- 이슈: 당시에는 GBN이 "rdt3.0을 여러 개 병렬로 보내는 것"이라고 생각했는데, 실제로 다른 점은 ACK 의미였다. rdt3.0은 개별 ACK이지만 GBN은 누적 ACK다 — "seq 3까지 다 받았다"라는 뜻이다.

### Session 2

- 목표: timeout 시 재전송 범위를 구현하고 이 비효율을 눈으로 확인한다.
- 진행:

```py
if timer_start and (time.time() - timer_start > TIMEOUT):
    print(f"[SENDER]   Timeout! Retransmitting packets {base} to {next_seq - 1}")
    for i in range(base, next_seq):
        channel_data.send(packets[i])
    timer_start = time.time()
```

- 이슈: 로그를 보니 seq 2만 손실됐는데 seq 2, 3, 4를 전부 다시 보내고 있었다. 3과 4는 이미 receiver가 받았는데도 GBN receiver는 out-of-order를 버리니까 또 받아야 한다. 이게 "비효율"의 실체였다. 동시에 다음 프로젝트(Selective Repeat)가 왜 필요한지를 뼈저리게 느낀 순간이기도 했다.
- 검증:

CLI:

```bash
$ make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-gbn
=== Go-Back-N (Window Size = 4) ===
[SENDER]   Sent packet seq=0: "Hello"
[SENDER]   Sent packet seq=1: "World"
[SENDER]   Sent packet seq=2: "RDT"
[SENDER]   Sent packet seq=3: "Protocol"
[RECEIVER] Received seq=0 → ACK 0
[RECEIVER] Received seq=1 → ACK 1
[SENDER]   ACK 1 received (cumulative)
[SENDER]   Timeout! Retransmitting packets 2 to 3
...
Status:   SUCCESS
```

```bash
$ make -C study/02-Reliable-Transport/rdt-protocol/problem test
===== 6 passed =====
```

- 정리:
  - rdt3.0의 핵심은 "timeout 후 똑같은 packet을 다시 보내는 discipline"이었다.
  - GBN의 핵심은 "누적 ACK 기준으로 window를 밀고, timeout 시 남은 전체를 재전송"이었다.
  - "seq 2만 죽었는데 3, 4도 다시 보낸다"는 로그를 직접 보니, Selective Repeat가 왜 필요한지가 교과서보다 설득력 있었다.
  - 다음 프로젝트에서 이 비효율을 정확히 선별적으로 고치는 작업을 한다.
