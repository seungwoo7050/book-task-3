# GBN vs Selective Repeat — 파이프라인 프로토콜 비교

## 개요

Go-Back-N(GBN)과 Selective Repeat(SR)는 모두 **슬라이딩 윈도우** 기반의 파이프라인 프로토콜이다. 과제에서 구현한 GBN의 한계를 이해하고, 대안인 SR과의 트레이드오프를 분석한다.

## 프로토콜 비교 표

| 특성 | GBN | Selective Repeat |
| :--- | :--- | :--- |
| 윈도우 크기 | 송신측만 N | 송신측 + 수신측 모두 N |
| ACK 방식 | 누적 ACK (cumulative) | 개별 ACK (individual) |
| 수신측 버퍼 | 없음 (순서 외 패킷 폐기) | 있음 (순서 외 패킷 버퍼링) |
| 타임아웃 재전송 | 윈도우 전체 재전송 | 해당 패킷만 재전송 |
| 타이머 | 1개 (최초 미확인 패킷) | 패킷당 1개 |
| 구현 복잡도 | 낮음 | 높음 |
| 불필요한 재전송 | 많음 | 없음 |
| 시퀀스 번호 범위 | $\geq N + 1$ | $\geq 2N$ |

## GBN의 동작 원리 (과제 구현)

### 송신측

```python
# 윈도우 내 패킷 전송
while next_seq < min(base + window_size, total):
    channel_data.send(packets[next_seq])
    next_seq += 1

# 타임아웃 시 윈도우 전체 재전송
if timeout:
    for i in range(base, next_seq):
        channel_data.send(packets[i])
```

### 수신측

```python
if seq == expected_seq:
    received.append(msg)
    channel_ack.send(make_ack(expected_seq))
    expected_seq += 1
else:
    # 순서 외 → 폐기 + 마지막 ACK 재전송
    channel_ack.send(make_ack(expected_seq - 1))
```

### GBN의 문제

```
Window = [3, 4, 5, 6]

pkt 3 → LOST
pkt 4 → 도착했지만 expected=3이므로 폐기!
pkt 5 → 도착했지만 expected=3이므로 폐기!
pkt 6 → 도착했지만 expected=3이므로 폐기!

→ TIMEOUT → pkt 3, 4, 5, 6 전부 재전송 (pkt 4, 5, 6은 불필요한 재전송)
```

## Selective Repeat의 개선

SR은 수신측에 **버퍼**를 두어 순서 외 패킷을 보관한다:

```
Window = [3, 4, 5, 6]

pkt 3 → LOST
pkt 4 → ACK 4 (버퍼에 저장)
pkt 5 → ACK 5 (버퍼에 저장)
pkt 6 → ACK 6 (버퍼에 저장)

pkt 3 TIMEOUT → pkt 3만 재전송
pkt 3 → ACK 3 → 버퍼의 4, 5, 6과 함께 순서대로 상위 레이어에 전달
```

### SR 수신측 로직 (의사 코드)

```python
if base <= seq < base + N:
    buffer[seq] = payload
    send_ack(seq)
    
    # 연속된 패킷이 있으면 상위에 전달
    while buffer[base] is not None:
        deliver(buffer[base])
        buffer[base] = None
        base += 1
```

## 시퀀스 번호 범위 문제

### GBN: $\text{seq range} \geq N + 1$

GBN은 누적 ACK을 사용하므로, 수신측이 마지막으로 확인한 패킷과 현재 윈도우를 구분하기 위해 $N + 1$개의 시퀀스 번호가 필요하다.

### SR: $\text{seq range} \geq 2N$

SR은 개별 ACK과 양쪽 윈도우를 사용하므로, 더 큰 시퀀스 번호 범위가 필요하다.

**예시** (N=3, seq range=3):
```
송신: [0, 1, 2] → 모두 도착, ACK 0/1/2 모두 손실
      → TIMEOUT → [0, 1, 2] 재전송
수신: 이미 0/1/2를 받았으므로 윈도우가 [3, 4, 5]로 이동
      → 새로 도착한 seq=0을 pkt 3으로 오인! ← 오류

해결: seq range ≥ 2N = 6 → [0, 1, 2, 3, 4, 5]
```

## TCP의 접근 방식

TCP는 GBN과 SR의 **하이브리드** 방식을 사용한다:

| 특성 | TCP |
| :--- | :--- |
| ACK 방식 | 누적 ACK (GBN 유사) + SACK 옵션 (SR 유사) |
| 수신 버퍼 | 있음 (SR과 동일) |
| 재전송 | 단일 패킷 (SR 유사) → Fast Retransmit |
| 타이머 | 1개 (GBN 유사) |

```
TCP의 Fast Retransmit:
3개 중복 ACK 수신 → 타임아웃 기다리지 않고 즉시 재전송
```

## 성능 비교

비신뢰 채널에서 N=4, 손실률 p일 때:

| 메트릭 | Stop-and-Wait | GBN | SR |
| :--- | :--- | :--- | :--- |
| 활용률 | $\frac{1-p}{1+2ap}$ | $\frac{N(1-p)}{1+2ap}$ | $\frac{N(1-p)}{(1-p)+Np}$ |
| 재전송 오버헤드 | 낮음 (1패킷) | 높음 (N패킷) | 최솟값 (1패킷) |
| 수신측 복잡도 | 최저 | 낮음 | 높음 |

여기서 $a = \frac{t_{prop}}{t_{trans}}$ (전파 지연 / 전송 지연 비율)

## 과제 구현에서의 선택

과제에서 GBN을 선택한 이유:
1. **수신측 단순성**: 버퍼 관리 없이 순서 외 패킷 폐기
2. **단일 타이머**: 타이머 관리가 간단
3. **누적 ACK**: ACK 손실에 대한 자연스러운 내성 (ACK 5가 도착하면 0~4도 확인)
4. **교재 순서**: 교과서에서 GBN → SR 순서로 다루며, GBN이 더 기초적 개념
