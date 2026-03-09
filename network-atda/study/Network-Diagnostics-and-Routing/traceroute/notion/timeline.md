# Traceroute — 개발 타임라인

## Phase 0: 환경 준비

```bash
python3 --version
# 표준 라이브러리: socket, struct, time, argparse, sys
# 테스트: pytest
pip install pytest

# raw socket → sudo 또는 CAP_NET_RAW 필요
```

## Phase 1: 설계 결정

- 전송: UDP 소켓 (포트 33434+, ttl별 고유 포트)
- 수신: Raw ICMP 소켓
- probe 매칭: ICMP 에러 메시지 내 원본 UDP dest port
- 종료 조건: ICMP Port Unreachable (type=3, code=3)

## Phase 2: 데이터 구조 정의

**작업 파일**: `python/src/traceroute.py`

```python
@dataclass
class ProbeObservation:
    responder: str | None     # 응답 IP
    rtt_ms: float | None      # RTT
    icmp_type: int | None     # ICMP type
    icmp_code: int | None     # ICMP code
```

## Phase 3: ICMP 응답 파서

**작업 함수**: `parse_icmp_response(packet: bytes)`

1. 외층 IP 헤더 → IHL 계산으로 건너뛰기
2. ICMP type, code 추출
3. ICMP 헤더(8B) 뒤에 내장된 원본 IP 헤더 → IHL 계산
4. 원본 UDP 헤더에서 dest port 추출
5. `(icmp_type, icmp_code, embedded_udp_dest_port)` 반환

## Phase 4: probe 포트 빌더

**작업 함수**: `build_probe_port(ttl, probe_index, probes_per_hop, base_port)`

```python
return base_port + (ttl - 1) * probes_per_hop + probe_index
```

- 각 probe에 고유한 포트 → ICMP 응답 매칭용

## Phase 5: hop 출력 포매터

**작업 함수**: `format_hop_line(ttl, observations)`

- 응답 있는 probe: RTT (ms)
- 타임아웃 probe: `*`
- responder IP 목록
- 포맷: `{ttl:2d}  {rtt1}  {rtt2}  {rtt3}  {ip}`

## Phase 6: trace_route 메인 로직

**작업 함수**: `trace_route(host, max_hops, probes_per_hop, timeout, base_port)`

1. `socket.gethostbyname(host)` — DNS 해석
2. Raw ICMP 수신 소켓 생성 + timeout
3. TTL 루프 (1 → max_hops):
   - 각 probe에 대해:
     a. UDP 소켓 생성, `IP_TTL` 설정
     b. 고유 포트로 `sendto()`
     c. ICMP 응답 대기 (`recvfrom`)
     d. `parse_icmp_response()`로 파싱
     e. embedded port와 매칭
   - 결과 포맷 후 출력
   - 목적지 IP + type=3, code=3이면 break

**CLI 확인**:
```bash
sudo python3 python/src/traceroute.py 8.8.8.8 --max-hops 15
```

## Phase 7: argparse CLI

```python
parser.add_argument("host")
parser.add_argument("--max-hops", type=int, default=30)
parser.add_argument("--probes", type=int, default=3)
parser.add_argument("--timeout", type=float, default=1.0)
parser.add_argument("--base-port", type=int, default=33434)
```

## Phase 8: 테스트

```bash
# 비권한 테스트: 파서, 포맷터, synthetic route
make -C problem test

# Live 테스트 (root 필요)
sudo make -C problem run-client HOST=8.8.8.8
```

**test_traceroute.py 검증 항목**:
- `parse_icmp_response()` 정확성 (fake ICMP 패킷)
- `build_probe_port()` 포트 고유성
- `format_hop_line()` 포맷 정확성
- synthetic 다중 hop 시나리오

## 최종 파일 구조

```
traceroute/
├── python/
│   ├── src/traceroute.py            ← 솔루션 (170줄)
│   └── tests/test_traceroute.py     ← deterministic pytest
├── problem/
│   ├── Makefile                     ← make test / sudo make run-client
│   ├── README.md                    ← 문제 사양
│   └── code/traceroute_skeleton.py  ← 제공 skeleton
├── docs/concepts/
└── notion/                          ← 이 문서
```
