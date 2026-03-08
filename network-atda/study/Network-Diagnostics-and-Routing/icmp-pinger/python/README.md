# Python 구현 안내

이 디렉터리는 `ICMP Pinger`의 공개 구현을 담는다.

## 구성

- `src/icmp_pinger.py`
- `tests/test_icmp_pinger.py`

## 기준 명령

- 실행: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- 검증: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 수동 live 검증: `sudo make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`

## 구현 메모

- 상태: `verified`
- 현재 범위: deterministic test가 checksum, packet build, reply parsing, RTT/statistics 출력 흐름까지 검증한다. raw socket live 실행은 수동 재현 명령으로 남긴다.
- 남은 약점: IPv6/ICMPv6 미지원
- 남은 약점: 시스템 ping 수준의 상세 통계 미지원
- 남은 약점: live raw-socket 실행은 OS/방화벽 정책에 영향받음
