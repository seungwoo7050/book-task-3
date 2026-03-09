# Selective Repeat — 선택적 재전송의 정밀함

## GBN에서 SR로

Go-Back-N을 구현하고 나면 한 가지 비효율이 눈에 밟힌다. 패킷 하나가 유실되면, 이미 성공적으로 전달된 이후 패킷들까지 전부 다시 보내야 한다. receiver가 순서를 벗어난 패킷을 버리기 때문이다. 대역폭이 귀한 환경에서 이 낭비는 치명적이다.

Selective Repeat(SR)은 이 문제를 정면으로 해결한다: receiver도 버퍼를 가지고 순서를 벗어난 패킷을 저장하며, sender는 타임아웃된 개별 패킷만 재전송한다. 대가는 복잡성의 증가다.

## 같은 채널, 다른 전략

이 프로젝트는 RDT Protocol과 동일한 `channel.py`와 `packet.py`를 재사용한다. 채널 모델이 같으므로, 프로토콜 로직의 차이가 성능 차이에 직접 반영된다. 공정한 비교를 위한 의도적 설계다.

## Sender의 변화: 개별 추적

GBN sender의 상태는 `base`와 `next_seq` 두 포인터뿐이었다. SR sender는 여기에 두 가지를 추가한다:

1. **`acked: set[int]`** — 개별 패킷의 ACK 수신 여부. GBN의 누적 ACK과 달리, "seq=5는 받았지만 seq=3은 아직"이라는 상태가 가능하다.
2. **`timers: dict[int, float]`** — 패킷별 독립 타이머. GBN은 가장 오래된 미확인 패킷 하나에 대한 타이머만 있었지만, SR은 각 패킷이 자기 타이머를 가진다.

ACK 수신 시 처리도 다르다. `acked.add(ack_seq)` 후, `send_base`가 연속으로 ACKed인 경우에만 슬라이드한다:

```python
while send_base in acked:
    acked.remove(send_base)
    send_base += 1
```

이것은 TCP의 cumulative ACK + SACK의 단순화된 버전이다.

## Receiver의 변화: 버퍼링과 순서 복원

GBN receiver는 상태가 `expected_seq` 하나였다. "기대하는 번호가 아니면 버린다." SR receiver는 윈도우 내의 모든 패킷을 받아들인다:

```python
if recv_base <= seq < recv_base + window_size:
    recv_buffer[seq] = payload.decode()
    channel_ack.send(make_ack(seq))    # 개별 ACK
```

버퍼에 저장한 후, `recv_base`부터 연속된 패킷이 있으면 순서대로 꺼내 전달한다:

```python
while recv_base in recv_buffer:
    delivered.append(recv_buffer.pop(recv_base))
    recv_base += 1
```

이 "연속 구간 소비" 패턴은 TCP 수신 버퍼의 핵심 메커니즘과 동일하다. 구멍(gap)이 채워지는 순간, 그 뒤에 버퍼링된 데이터가 한꺼번에 애플리케이션 계층으로 올라간다.

### 윈도우 밖의 중복 처리

`seq < recv_base`인 패킷이 도착하면? 이것은 이전에 정상 수신했지만 ACK가 유실된 패킷의 재전송이다. receiver는 다시 ACK를 보낸다 — 그래야 sender가 그 패킷의 타이머를 멈추고 윈도우를 진행할 수 있다.

## 타이머 관리의 복잡성

GBN에서 타이머 코드는 2줄이었다. SR에서는 매 루프 반복마다 미확인 패킷 전체를 순회한다:

```python
for seq in range(send_base, next_seq):
    if seq in acked:
        continue
    if now - timers[seq] > TIMEOUT:
        channel_data.send(packets[seq])
        timers[seq] = time.time()
```

해당 패킷만 재전송하고, 해당 패킷의 타이머만 리셋한다. 이것이 "selective"의 의미다.

## GBN vs SR — 관찰되는 차이

동일한 채널 설정(loss=0.2, corrupt=0.1)에서:

- **GBN**: 타임아웃 발생 시 `"Retransmitting packets 3 to 7"` — 범위 재전송
- **SR**: 타임아웃 발생 시 `"Retransmitting seq=3"` — 개별 재전송

손실률이 높아질수록 차이가 극적이다. GBN의 재전송 오버헤드는 `O(window_size)`이지만, SR은 `O(1)`이다. 대신 SR은 receiver 메모리를 윈도우 크기만큼 사용한다.

## 테스트

단위 테스트는 두 가지를 확인한다:

1. 무손실 채널에서 모든 메시지가 순서대로 전달되는가
2. `load_messages()`로 테스트 데이터를 로드할 수 있는가

통합 테스트(`test_selective_repeat.sh`)는 실제 손실/손상 채널에서 실행하여 "SUCCESS" 출력을 검증한다.

## Reliable Transport 트랙의 완성

RDT 3.0 → GBN → SR. 세 프로토콜을 같은 인프라 위에서 순차적으로 구현하면서, 각 단계에서 이전 설계의 한계가 다음 설계의 동기가 되는 것을 경험했다. Stop-and-Wait의 낮은 utilization이 파이프라인을 낳고, GBN의 불필요한 재전송이 SR을 낳는다. TCP는 이 모든 교훈 위에 서 있다.
