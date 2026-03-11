# ICMP Pinger — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: socket, struct, os, select, sys, time
# 테스트: pytest
pip install pytest

# raw socket 권한 확인
# macOS: sudo 필요
# Linux: sudo 또는 CAP_NET_RAW capability
```

## Phase 1: skeleton 분석

**파일**: `problem/code/icmp_pinger_skeleton.py`

- ICMP 상수 정의: `ICMP_ECHO_REQUEST = 8`, `ICMP_ECHO_REPLY = 0`
- `ICMP_HEADER_FORMAT = "!BBHHH"` — Type, Code, Checksum, ID, Sequence
- 빈 함수: `internet_checksum()`, `build_echo_request()`, `parse_echo_reply()`, `ping()`

## Phase 2: 인터넷 체크섬 구현

**작업 함수**: `internet_checksum(data: bytes) -> int`

1. 홀수 길이 패딩: `data += b"\x00"`
2. 2바이트씩 빅엔디안으로 읽어 누적 합산
3. 캐리 폴딩: `while total >> 16: total = (total & 0xFFFF) + (total >> 16)`
4. 비트 반전: `~total & 0xFFFF`

**단위 테스트 확인**:
```bash
cd python/tests && python3 -m pytest test_icmp_pinger.py -k checksum -v
```

## Phase 3: Echo Request 패킷 빌드

**작업 함수**: `build_echo_request(identifier: int, sequence: int) -> bytes`

1. 체크섬 0으로 헤더 임시 생성: `struct.pack("!BBHHH", 8, 0, 0, id, seq)`
2. 페이로드: `struct.pack("!d", time.time())` — 현재 시각 8바이트 double
3. `internet_checksum(header + payload)` 계산
4. 올바른 체크섬으로 헤더 재생성
5. `header + payload` 반환

## Phase 4: Echo Reply 파싱

**작업 함수**: `parse_echo_reply(data: bytes, identifier: int) -> tuple | None`

1. IP 헤더 길이 계산: `(data[0] & 0x0F) * 4`
2. IP 헤더 이후부터 ICMP 헤더 읽기: `struct.unpack("!BBHHH", ...)`
3. type이 0(Echo Reply)이고 id가 일치하는지 확인
4. 페이로드에서 타임스탬프 추출: `struct.unpack("!d", ...)`
5. `(sequence, send_time)` 반환, 불일치 시 `None`

## Phase 5: raw socket 생성 및 ping 루프

**작업 함수**: `ping(host: str, count: int, timeout: float)`

1. `socket.gethostbyname(host)` — DNS → IP 해석
2. `socket.socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)` — raw ICMP 소켓
3. `PermissionError` catch → "sudo 필요" 안내 메시지
4. `identifier = os.getpid() & 0xFFFF` — PID 기반 식별자

**ping 루프**:
```
for seq in range(1, count + 1):
    packet = build_echo_request(identifier, seq)
    raw_socket.sendto(packet, (dest_ip, 0))
    ready = select.select([raw_socket], [], [], timeout)
    if ready:
        data, addr = raw_socket.recvfrom(1024)
        result = parse_echo_reply(data, identifier)
        → RTT 계산, 출력
    else:
        → "Request timed out"
    sleep(1초 간격 보장)
```

**CLI 확인**:
```bash
sudo python3 python/src/icmp_pinger.py google.com -c 4
# → 각 핑의 RTT + 통계 출력
```

## Phase 6: 통계 출력

1. `rtt_list`에서 min/avg/max 계산
2. 손실률: `(sent - received) / sent * 100`
3. 응답 없음 시 별도 메시지

## Phase 7: CLI 인터페이스

```python
target_host = sys.argv[1]
# -c 옵션으로 ping 횟수 지정
if "-c" in sys.argv:
    idx = sys.argv.index("-c")
    ping_count = int(sys.argv[idx + 1])
```

**사용법**:
```bash
sudo python3 icmp_pinger.py google.com          # 기본 4회
sudo python3 icmp_pinger.py google.com -c 10     # 10회
```

## Phase 8: 테스트 (2계층)

### 비권한 deterministic 테스트
```bash
make -C problem test
# → pytest로 checksum, packet build, reply parse 검증
# → root 권한 불필요
```

### Live raw-socket 테스트
```bash
sudo make -C problem test-live HOST=google.com
# → 실제 ICMP 핑을 보내 응답 확인
# → root 권한 필요
```

## 최종 파일 구조

```
icmp-pinger/
├── python/
│   ├── src/icmp_pinger.py           ← 솔루션 (210줄)
│   └── tests/test_icmp_pinger.py    ← deterministic pytest
├── problem/
│   ├── Makefile                     ← make test / sudo make test-live
│   ├── code/icmp_pinger_skeleton.py ← 제공 skeleton
│   └── script/test_icmp.sh          ← live 검증 스크립트
├── docs/concepts/
└── notion/                          ← 이 문서
```
