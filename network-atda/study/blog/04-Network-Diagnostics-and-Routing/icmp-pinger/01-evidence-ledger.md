# ICMP Pinger Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/README.md`
- 구현 엔트리: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`
- 보조 테스트: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`
- 실행 표면: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/Makefile`
- live harness: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/script/test_icmp.sh`

## 핵심 코드 근거

- `internet_checksum()`: 16-bit word 합산, carry fold, one's complement를 직접 구현한다.
- `build_echo_request()`: checksum placeholder header를 만든 뒤 payload timestamp와 합쳐 checksum을 다시 채운다.
- `parse_echo_reply()`: outer IP header length를 먼저 읽은 뒤 ICMP type/id/sequence와 embedded timestamp를 복원한다.
- `ping()`: `select.select()`로 timeout을 관리하고, 성공 시 RTT 통계 리스트를 누적해 summary를 출력한다.

## 테스트 근거

`make -C network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`

결과:

- `11 passed in 0.01s`

세부:

- checksum known-value, all-zero, verify-zero, odd-length cases 통과
- packet type/code/checksum/id/sequence validation 통과
- fake raw socket test에서 `50.0% loss`와 `RTT min/avg/max = 50.000/50.000/50.000 ms` 출력 검증
- `test_icmp.sh`는 root + live network가 있을 때 `Ping completes successfully`, `RTT measurements`, `ping statistics`를 확인하는 별도 harness다

보조 실행:

- `python3 python/src/icmp_pinger.py example.com -c 1`은 현재 세션에서 5초 내 완료되지 않았다

## 이번에 고정한 해석

- 이 lab의 핵심은 "ping output을 흉내 낸다"가 아니라, packet binary contract와 통계를 함께 직접 책임지는 것이다.
- deterministic tests가 훨씬 강한 근거이고, live path는 환경 의존적인 supplemental check로 남겨야 한다.
- raw socket lab답게 권한과 network environment가 구현 correctness와 별도로 문서화돼야 한다.
- 즉 `make test` 통과와 live internet probe 성공은 서로 다른 수준의 증거다.
