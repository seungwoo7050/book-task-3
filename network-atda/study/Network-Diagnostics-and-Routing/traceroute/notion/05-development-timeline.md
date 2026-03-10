# 05 개발 타임라인

이 문서는 `Traceroute`를 처음 재현하는 학생을 위한 실행 가이드다. 핵심은 raw socket이 필요한 live trace와, 권한 없이도 돌릴 수 있는 parser/formatting 테스트를 분리해서 확인하는 것이다.

## 준비
- `python3`
- `pytest`
- live 실행용 관리자 권한 또는 raw socket 권한
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/traceroute_skeleton.py`](../problem/code/traceroute_skeleton.py)
- [`../docs/concepts/ipv4-header.md`](../docs/concepts/ipv4-header.md)
- [`../docs/concepts/icmp-protocol.md`](../docs/concepts/icmp-protocol.md)

여기서 확인할 질문:
- 왜 TTL을 1부터 늘려 가는가
- 왜 UDP 송신과 raw ICMP 수신을 같이 써야 하는가
- 도착지 판정은 어떤 ICMP 메시지로 하는가

## 단계 2. 구현과 테스트 기준을 먼저 본다
- [`../python/src/traceroute.py`](../python/src/traceroute.py)
- [`../python/tests/test_traceroute.py`](../python/tests/test_traceroute.py)

이 단계에서 볼 포인트:
- probe port를 어떻게 만든는가
- nested ICMP payload에서 원래 UDP 포트를 어디서 읽는가
- `*` timeout과 정상 hop 출력이 어떤 formatter로 묶이는가

## 단계 3. 권한 없는 자동 검증 먼저 실행
아래 명령으로 parser, formatter, synthetic integration을 먼저 확인한다.

```bash
make -C study/Network-Diagnostics-and-Routing/traceroute/problem test
```

기대 결과:
- 포트 생성 규칙 테스트가 통과한다.
- ICMP 응답 파싱과 hop 출력 테스트가 통과한다.
- synthetic route 종료 조건 검증이 통과한다.

## 단계 4. live traceroute 실행
권한이 있는 환경이면 아래를 실행한다.

```bash
make -C study/Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8 MAX_HOPS=8 PROBES=3 TIMEOUT=1.0
```

기대 결과:
- hop 번호가 한 줄씩 출력된다.
- 응답이 없는 probe는 `*`로 표시될 수 있다.
- 목적지에 도달하면 더 이상 불필요한 probe를 보내지 않는다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- 권한 오류가 나면 raw socket 실행 환경부터 확인한다.
- hop 매칭이 이상하면 embedded UDP destination port 파싱을 먼저 본다.
- 목적지에 도착했는데 계속 진행되면 ICMP `type=3`, `code=3` 종료 조건을 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- 권한 없는 테스트가 통과한다.
- 권한이 있는 환경에서 live traceroute를 한 번 실행했다.
- TTL, ICMP Time Exceeded, Port Unreachable의 관계를 설명할 수 있다.
- probe 매칭에 destination port가 왜 필요한지 설명할 수 있다.
