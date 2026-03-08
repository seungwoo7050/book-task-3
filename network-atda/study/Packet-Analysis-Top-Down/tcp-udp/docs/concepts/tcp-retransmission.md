# TCP 재전송 메커니즘 심층 분석

## 개요

TCP는 신뢰성 있는 데이터 전송을 보장하기 위해 여러 재전송 메커니즘을 활용한다.
이 문서는 Wireshark 캡처에서 관찰할 수 있는 재전송 이벤트의 유형, 트리거 조건,
그리고 성능에 미치는 영향을 분석한다.

---

## 1. 타임아웃 기반 재전송 (RTO)

### 동작 원리

송신자가 세그먼트를 전송한 후 **Retransmission Timeout (RTO)** 내에
ACK를 수신하지 못하면 해당 세그먼트를 재전송한다.

### RTO 계산

```
SRTT = (1 - α) × SRTT + α × SampleRTT          (α = 0.125)
DevRTT = (1 - β) × DevRTT + β × |SampleRTT - SRTT|  (β = 0.25)
RTO = SRTT + 4 × DevRTT
```

- **SRTT (Smoothed RTT)**: 평활화된 왕복 시간
- **DevRTT**: RTT 편차의 추정값
- **최소 RTO**: 일반적으로 1초 (RFC 6298)

### 지수적 백오프 (Exponential Backoff)

연속 타임아웃 발생 시 RTO를 2배씩 증가시킨다:

```
타임아웃 1회: RTO
타임아웃 2회: 2 × RTO
타임아웃 3회: 4 × RTO
...
```

### Wireshark에서 관찰

- **필터**: `tcp.analysis.retransmission`
- 재전송 세그먼트는 이전에 전송된 시퀀스 번호와 동일한 시퀀스 번호를 가진다
- Info 컬럼에 `[TCP Retransmission]` 표시

---

## 2. 빠른 재전송 (Fast Retransmit)

### 동작 원리

3개의 **중복 ACK (Duplicate ACK)** 를 수신하면 타임아웃을 기다리지 않고
즉시 해당 세그먼트를 재전송한다.

### 시나리오 예시

```
송신: Seq=100, Seq=200, Seq=300, Seq=400, Seq=500
       ↑ 이 세그먼트 손실

수신 → ACK=200 (정상)
수신 → ACK=200 (중복 1 — Seq=300 수신했지만 200을 기대)
수신 → ACK=200 (중복 2 — Seq=400 수신)
수신 → ACK=200 (중복 3 — Seq=500 수신)

→ 3개 중복 ACK 수신: Seq=200 빠른 재전송 트리거
```

### Wireshark에서 관찰

- **중복 ACK 필터**: `tcp.analysis.duplicate_ack`
- **빠른 재전송 필터**: `tcp.analysis.fast_retransmission`
- 3번째 중복 ACK 직후에 재전송 발생하는 패턴 확인

### 빠른 회복 (Fast Recovery)

Fast Retransmit 후 혼잡 윈도우를 절반으로 줄이고(Slow Start 임계값 설정),
곧바로 **혼잡 회피 (Congestion Avoidance)** 단계로 진입한다:

```
ssthresh = cwnd / 2
cwnd = ssthresh + 3 × MSS    (중복 ACK 3개에 대한 인플레이션)
```

---

## 3. SACK (Selective Acknowledgment)

### 기존 누적 ACK의 한계

누적 ACK는 "이 바이트까지 모두 수신함"만 알려주므로,
중간에 빠진 세그먼트 이후의 정상 수신 세그먼트를 식별할 수 없다.

### SACK 동작

TCP 옵션 필드에 수신한 비순차(out-of-order) 블록의 범위를 명시한다:

```
ACK=200, SACK=300-500, 700-900
→ "200까지 수신, 300-500과 700-900도 수신했지만 200-300과 500-700이 빠짐"
```

### 이점

| 항목 | 누적 ACK만 사용 | SACK 사용 |
| :--- | :--- | :--- |
| 재전송 범위 | 손실 이후 전체 | 실제 손실 세그먼트만 |
| 불필요한 재전송 | 많음 | 최소화 |
| 다중 손실 대응 | RTO 의존 | 한 번의 RTT로 복구 가능 |

### Wireshark에서 관찰

- **필터**: `tcp.options.sack`
- TCP 옵션 > SACK 블록 확인: Left Edge, Right Edge 값

### 3-way 핸드셰이크에서 SACK 협상

```
SYN:     SACK Permitted (옵션 Kind=4)
SYN-ACK: SACK Permitted (옵션 Kind=4)
→ 양쪽 모두 동의해야 SACK 사용 가능
```

---

## 4. Spurious 재전송

### 정의

실제로 손실되지 않았지만 불필요하게 재전송된 세그먼트이다.

### 발생 원인

- **RTT 급증**: 네트워크 지연 변동으로 RTO 초과
- **ACK 재정렬**: ACK 패킷이 지연되어 도착
- **경로 변경**: 네트워크 경로 전환 시 일시적 지연 증가

### Wireshark에서 관찰

- **필터**: `tcp.analysis.spurious_retransmission`
- 원본 세그먼트의 ACK가 이미 도착한 후에 재전송이 발생하는 패턴

---

## 5. 재전송과 성능 관계

### 재전송률 계산

```
재전송률 = 재전송 세그먼트 수 / 전체 세그먼트 수 × 100%
```

### 성능 영향

| 재전송률 | 네트워크 상태 | 예상 원인 |
| :--- | :--- | :--- |
| < 1% | 정상 | 간헐적 손실 |
| 1–5% | 경고 | 혼잡 발생 가능 |
| > 5% | 심각 | 네트워크 혼잡 또는 장애 |

### Wireshark 통계 활용

- **Statistics → TCP Stream Graphs → Time-Sequence (tcptrace)**: 재전송 지점을 시각적으로 확인
- **Statistics → I/O Graphs**: 재전송 빈도를 시간축에 매핑

---

## 6. 실습과의 연결

TCP/UDP Wireshark 실습에서 관찰 가능한 재전송 관련 포인트:

1. **3-way 핸드셰이크 분석** 시 SACK Permitted 옵션 확인
2. **데이터 전송 중** 시퀀스 번호 반복으로 재전송 식별
3. **처리량 계산** 시 재전송이 유효 처리량(goodput)에 미치는 영향 고려
4. **혼잡 윈도우 그래프**에서 Fast Retransmit 후 cwnd 감소 패턴 관찰
5. **TCP vs UDP 비교** 시 재전송 메커니즘이 없는 UDP의 특성 대비
