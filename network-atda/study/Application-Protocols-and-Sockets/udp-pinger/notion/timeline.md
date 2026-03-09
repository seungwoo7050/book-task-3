# UDP Pinger — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리만 사용: socket, sys, time
# 테스트용: pytest 설치
pip install pytest
```

프로젝트 구조:
- `problem/code/udp_pinger_server.py` — 제공 서버 (수정 불가)
- `problem/code/udp_pinger_client_skeleton.py` — 빈 skeleton
- `python/src/udp_pinger_client.py` — 솔루션 작성 위치

## Phase 1: 제공 서버 분석

**파일**: `problem/code/udp_pinger_server.py`

1. `socket.socket(AF_INET, SOCK_DGRAM)` — UDP 소켓
2. `recvfrom(1024)` — 클라이언트 메시지 수신
3. `random.randint(1, 10) <= 3` — 30% 확률로 패킷 드롭
4. 에코: 메시지를 대문자로 변환 후 `sendto()`로 반환

**CLI 확인**:
```bash
python3 problem/code/udp_pinger_server.py 12000
# → [INFO] UDP Pinger Server started on port 12000
```

## Phase 2: UDP 클라이언트 소켓 생성

**작업 파일**: `python/src/udp_pinger_client.py`

1. `socket.socket(AF_INET, SOCK_DGRAM)` — UDP 소켓 생성
2. `client_socket.settimeout(1)` — 1초 타임아웃 (손실 판정 기준)
3. 상수 정의: `PING_COUNT = 10`, `TIMEOUT = 1`

## Phase 3: 핑 메시지 전송 루프

1. `for seq in range(1, 11)` — 10회 반복
2. 메시지 포맷: `f"Ping {seq} {time.time()}"`
3. `client_socket.sendto(message.encode(), server_address)`
4. `client_socket.recvfrom(1024)` — 응답 대기
5. `socket.timeout` 예외 처리 — "Request timed out" 출력

## Phase 4: RTT 계산

1. `send_time = time.time()` — 전송 직전 타임스탬프
2. 응답 수신 시 `recv_time = time.time()` 
3. `rtt_ms = (recv_time - send_time) * 1000` — 밀리초 변환
4. `rtt_list.append(rtt_ms)` — 리스트에 누적

## Phase 5: 통계 출력

1. `sent = PING_COUNT`, `received = len(rtt_list)`
2. `loss_pct = (lost / sent) * 100` — 손실률
3. `min(rtt_list)`, `max(rtt_list)`, `sum()/len()` — min/avg/max RTT
4. `rtt_list`가 비어있을 경우 "No replies received" 분기 처리

## Phase 6: CLI 인자 처리

```python
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
```

## Phase 7: 통합 테스트

**작업 파일**: `python/tests/test_udp_pinger.py`

```bash
# 터미널 1: 서버 기동
python3 problem/code/udp_pinger_server.py 12000

# 터미널 2: 솔루션 실행
python3 python/src/udp_pinger_client.py 127.0.0.1 12000

# 터미널 3: pytest 실행
cd python/tests && python3 -m pytest test_udp_pinger.py -v
```

## Phase 8: Makefile 검증

```bash
# 자동 검증: 서버 백그라운드 기동 → 클라이언트 실행 → 출력 검사
make -C problem test
```

내부 동작:
1. `udp_pinger_server.py`를 백그라운드로 시작
2. `script/test_pinger.sh`가 솔루션 실행 후 출력에서 "Ping", "loss", "RTT" 키워드 검증
3. `trap`으로 서버 자동 종료

## 최종 파일 구조

```
udp-pinger/
├── python/
│   ├── src/udp_pinger_client.py    ← 솔루션 (80줄)
│   └── tests/test_udp_pinger.py    ← pytest 테스트
├── problem/
│   ├── Makefile                    ← make test / make run-solution
│   ├── code/
│   │   ├── udp_pinger_server.py    ← 제공 서버 (수정불가)
│   │   └── udp_pinger_client_skeleton.py
│   └── script/test_pinger.sh       ← bash 검증 스크립트
├── docs/concepts/
└── notion/                         ← 이 문서
```
