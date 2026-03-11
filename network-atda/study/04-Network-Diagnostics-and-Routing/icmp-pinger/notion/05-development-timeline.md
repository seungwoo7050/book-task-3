# 05 개발 타임라인

이 문서는 `ICMP Pinger`를 처음 재현하는 학생을 위한 실행 가이드다. 핵심은 권한이 필요 없는 테스트와 실제 raw socket 실행을 분리해서 보는 것이다.

## 준비
- `python3`
- `pytest`
- live 실행용 관리자 권한 또는 `CAP_NET_RAW`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/icmp_pinger_skeleton.py`](../problem/code/icmp_pinger_skeleton.py)
- [`../docs/concepts/checksum.md`](../docs/concepts/checksum.md)
- [`../docs/concepts/raw-sockets.md`](../docs/concepts/raw-sockets.md)

여기서 확인할 질문:
- 어떤 부분을 직접 바이트 수준에서 만들어야 하는가
- 왜 raw socket 권한이 필요한가
- deterministic test와 live test를 왜 분리하는가

## 단계 2. 구현과 테스트 기준을 먼저 본다
- [`../python/src/icmp_pinger.py`](../python/src/icmp_pinger.py)
- [`../python/tests/test_icmp_pinger.py`](../python/tests/test_icmp_pinger.py)

이 단계에서 볼 포인트:
- checksum 함수가 어디 있는가
- 응답 파싱에서 `IHL`을 어떻게 쓰는가
- 성공 응답과 전손실 출력이 각각 어떻게 검증되는가

## 단계 3. 권한 없는 자동 검증 먼저 실행
먼저 raw socket이 필요 없는 테스트부터 돌린다.

```bash
make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test
```

기대 결과:
- checksum, packet build, 출력 포맷 테스트가 통과한다.
- 루트 권한 없이도 현재 구현의 핵심 로직을 확인할 수 있다.

## 단계 4. live raw-socket 실행
권한이 있는 환경이면 아래를 실행한다.

```bash
sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=8.8.8.8 COUNT=4
sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=8.8.8.8
```

기대 결과:
- Echo Reply 라인이 반복 출력된다.
- 마지막에 packet loss와 RTT 통계가 나온다.
- `test-live`는 live 검증 결과를 통과하거나, 권한이 없으면 명시적으로 skip를 안내한다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- 응답이 전혀 없으면 권한, 방화벽, 대상 호스트를 먼저 확인한다.
- 응답 파싱이 이상하면 `IHL * 4` 계산과 identifier/sequence 비교를 먼저 본다.
- checksum 문제는 [`../docs/concepts/checksum.md`](../docs/concepts/checksum.md)와 [`02-debug-log.md`](02-debug-log.md)를 함께 본다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- 비권한 테스트가 통과한다.
- 권한이 있는 환경에서 live 실행을 한 번 해봤다.
- checksum과 `IHL` 파싱이 왜 중요한지 설명할 수 있다.
- 왜 deterministic test와 live test를 분리했는지 설명할 수 있다.
