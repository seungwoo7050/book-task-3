# RDT 3.0 & Go-Back-N — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: hashlib, struct, random, time, argparse
# 테스트: pytest
pip install pytest
```

**제공 코드 분석**:
```bash
ls problem/code/
# channel.py        ← UnreliableChannel (loss, corrupt, delay)
# packet.py         ← make_packet, parse_packet, is_corrupt, make_ack, is_ack
# rdt3_skeleton.py  ← RDT 3.0 시작 템플릿
# gbn_skeleton.py   ← GBN 시작 템플릿
```

## Phase 1: 패킷 모듈 이해

**패킷 포맷**: `[checksum 4B][seq_num 4B][payload]`
- checksum = `hashlib.md5(struct.pack("!I", seq) + payload).digest()[:4]`
- `struct.pack("!4sI", checksum, seq_num)` — 네트워크 바이트 오더

```bash
python3 -c "
from problem.code.packet import make_packet, parse_packet, is_corrupt
pkt = make_packet(0, b'Hello')
print(f'Packet length: {len(pkt)}')
cs, seq, payload = parse_packet(pkt)
print(f'seq={seq}, payload={payload}, corrupt={is_corrupt(pkt)}')
"
```

## Phase 2: 채널 모듈 이해

```python
# channel.py 핵심 동작
ch = UnreliableChannel(loss_rate=0.2, corrupt_rate=0.1)
ch.send(packet)       # delay → loss 확률 → corrupt 확률 → _buffer에 저장
ch.has_packet()       # _buffer 비어있는지 확인
ch.receive()          # _buffer.pop(0)
```

- corruption: `bytearray[random_idx] ^= (1 << random_bit)`
- FIFO 큐 기반, 순서 보존

## Phase 3: RDT 3.0 (Stop-and-Wait) 구현

**작업 파일**: `python/src/rdt3.py`

### 상태 변수 설계
```
Sender: send_seq (0 or 1), send_idx, current_pkt, timer_start, awaiting_ack
Receiver: expected_seq (0 or 1)
```

### 이벤트 루프 구현
1. `channel_data.has_packet()` → receiver 처리
   - 정상 + 기대 seq → 수신 리스트에 추가, ACK 전송, expected_seq 반전
   - 중복/손상 → 이전 ACK 재전송 (`1 - expected_seq`)
2. `channel_ack.has_packet()` → sender 처리
   - `is_ack(pkt, send_seq)` → seq 반전, 다음 패킷 전송
3. timeout 체크 → 현재 패킷 재전송

### 초기 테스트
```bash
python3 python/src/rdt3.py --loss 0 --corrupt 0
# → 손실/손상 없이 정상 전달 확인

python3 python/src/rdt3.py --loss 0.3 --corrupt 0.2
# → 재전송 로그 확인, 최종 SUCCESS 확인
```

## Phase 4: Go-Back-N 구현

**작업 파일**: `python/src/gbn.py`

### RDT 3.0과의 차이점
- 시퀀스 번호: alternating bit → 순차 정수
- 패킷 미리 빌드: `packets = [make_packet(i, data[i].encode()) for i in range(total)]`
- 윈도우: `base`, `next_seq` 포인터
- ACK: 개별 → 누적 (cumulative)
- 타임아웃: 단일 패킷 → `base..next_seq-1` 범위 재전송

### 윈도우 전송 로직
```python
while next_seq < min(base + window_size, total):
    channel_data.send(packets[next_seq])
    if base == next_seq:
        timer_start = time.time()   # 첫 패킷에만 타이머 시작
    next_seq += 1
```

### receiver 로직
- `seq == expected_seq` → 수신, ACK, `expected_seq += 1`
- 그 외 → 마지막 정상 ACK 재전송 (`expected_seq - 1`)
- `expected_seq == 0`일 때 예외 처리 (보낼 ACK 없음)

### 테스트
```bash
python3 python/src/gbn.py --loss 0.2 --corrupt 0.1 --window 4
python3 python/src/gbn.py --loss 0.2 --corrupt 0.1 --window 8
# 윈도우 크기에 따른 성능 차이 관찰
```

## Phase 5: 테스트 데이터

```bash
cat problem/data/test_messages.txt
# 여러 줄의 테스트 메시지 — 양쪽 프로토콜이 공유
```

## Phase 6: 단위 테스트

```bash
cd python/tests
python3 -m pytest test_rdt.py -v
# TestPacketModule:
#   test_make_and_parse_packet
#   test_valid_packet_not_corrupt
#   test_corrupted_packet_detected
#   test_make_ack
#   test_is_ack_valid
#   test_is_ack_wrong_seq
#   test_different_seq_different_checksum
```

## Phase 7: 통합 테스트

```bash
make -C problem test
# → bash script/test_rdt.sh
# → RDT 3.0 실행 + SUCCESS 확인
# → GBN 실행 + SUCCESS 확인
```

## Phase 8: 비교 실험

```bash
# 손실률 변화에 따른 성능
python3 python/src/rdt3.py --loss 0.1 --corrupt 0.05
python3 python/src/rdt3.py --loss 0.3 --corrupt 0.15

python3 python/src/gbn.py --loss 0.1 --corrupt 0.05 --window 4
python3 python/src/gbn.py --loss 0.3 --corrupt 0.15 --window 4

# GBN 높은 손실에서의 재전송 폭발 관찰
python3 python/src/gbn.py --loss 0.4 --corrupt 0.2 --window 8
```

## 최종 파일 구조

```
rdt-protocol/
├── python/
│   ├── src/
│   │   ├── rdt3.py              ← RDT 3.0 솔루션 (~130줄)
│   │   └── gbn.py               ← GBN 솔루션 (~150줄)
│   └── tests/
│       └── test_rdt.py          ← packet 모듈 단위 테스트
├── problem/
│   ├── Makefile                 ← run-solution-rdt3 / run-solution-gbn / test
│   ├── code/
│   │   ├── channel.py           ← 비신뢰 채널 (제공)
│   │   ├── packet.py            ← 패킷 유틸리티 (제공)
│   │   ├── rdt3_skeleton.py     ← skeleton
│   │   └── gbn_skeleton.py      ← skeleton
│   ├── data/
│   │   └── test_messages.txt    ← 공유 테스트 데이터
│   └── script/
│       └── test_rdt.sh          ← 통합 검증
├── docs/concepts/
└── notion/                      ← 이 문서
```
