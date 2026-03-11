# Selective Repeat — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
pip install pytest
```

**기존 인프라 재사용 확인**:
```bash
ls ../rdt-protocol/problem/code/
# channel.py  packet.py  ← 동일 모듈 재사용
ls problem/code/
# channel.py  packet.py  selective_repeat_skeleton.py
```

## Phase 1: GBN과의 차이점 설계

| 측면 | GBN | SR (목표) |
|------|-----|-----------|
| ACK | 누적 (cumulative) | 개별 (individual) |
| receiver | expected_seq만 수신, 나머지 폐기 | 윈도우 내 모든 패킷 버퍼링 |
| 타이머 | 전체 윈도우 하나 | 패킷별 독립 타이머 |
| 재전송 | base~next_seq 전체 | 타임아웃된 패킷만 |

## Phase 2: Sender 상태 설계

```python
# GBN에서 추가된 상태
acked: set[int] = set()              # 개별 ACK 추적
timers: dict[int, float] = {}        # 패킷별 타이머
```

### 윈도우 전송 (GBN과 동일)
```python
while next_seq < min(send_base + window_size, total):
    channel_data.send(packets[next_seq])
    timers[next_seq] = time.time()   # 개별 타이머 시작
    next_seq += 1
```

### ACK 처리 (GBN과 다름)
```python
acked.add(ack_seq)
timers.pop(ack_seq, None)
while send_base in acked:   # 연속 ACK 구간만 슬라이드
    acked.remove(send_base)
    send_base += 1
```

## Phase 3: Receiver 버퍼 구현

```python
recv_base = 0
recv_buffer: dict[int, str] = {}
```

### 수신 로직
1. `recv_base <= seq < recv_base + window_size` → 버퍼 저장 + 개별 ACK
2. `seq < recv_base` → 이전 ACK 재전송 (sender 복구 지원)
3. 나머지 → 무시

### 순서 복원 (in-order delivery)
```python
while recv_base in recv_buffer:
    delivered.append(recv_buffer.pop(recv_base))
    recv_base += 1
```

## Phase 4: 개별 타이머 처리

```python
now = time.time()
for seq in range(send_base, next_seq):
    if seq in acked:
        continue
    if now - timers[seq] > TIMEOUT:
        channel_data.send(packets[seq])   # 해당 패킷만 재전송
        timers[seq] = time.time()
```

## Phase 5: 초기 테스트

```bash
# 무손실 테스트
python3 python/src/selective_repeat.py --loss 0 --corrupt 0 --window 4

# 기본 손실 테스트
python3 python/src/selective_repeat.py --loss 0.2 --corrupt 0.1 --window 4
# → 개별 재전송 로그 확인: "Retransmitting seq=X"
```

## Phase 6: 단위 테스트

```bash
cd python/tests
python3 -m pytest test_selective_repeat.py -v
# test_selective_repeat_delivers_all_messages_without_loss
# test_message_fixture_is_available
```

## Phase 7: 통합 테스트

```bash
make -C problem test
# → bash script/test_selective_repeat.sh
# → SUCCESS 확인
```

## Phase 8: GBN과의 비교 실험

```bash
# 높은 손실률에서 차이 관찰
python3 ../rdt-protocol/python/src/gbn.py --loss 0.4 --corrupt 0.2 --window 8
python3 python/src/selective_repeat.py --loss 0.4 --corrupt 0.2 --window 8
# → GBN: 범위 재전송 다수 vs SR: 개별 재전송만
```

## 최종 파일 구조

```
selective-repeat/
├── python/
│   ├── src/
│   │   └── selective_repeat.py           ← 솔루션 (~140줄)
│   └── tests/
│       └── test_selective_repeat.py      ← 단위 테스트
├── problem/
│   ├── Makefile                          ← run-solution / test
│   ├── code/
│   │   ├── channel.py                    ← 비신뢰 채널 (재사용)
│   │   ├── packet.py                     ← 패킷 유틸리티 (재사용)
│   │   └── selective_repeat_skeleton.py  ← skeleton
│   ├── data/
│   │   └── test_messages.txt             ← 공유 테스트 데이터
│   └── script/
│       └── test_selective_repeat.sh      ← 통합 검증
├── docs/concepts/
└── notion/                               ← 이 문서
```
