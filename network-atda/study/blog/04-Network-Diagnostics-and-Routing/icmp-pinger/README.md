# ICMP Pinger Blog

이 문서 묶음은 `icmp-pinger`를 "ping 비슷한 도구를 만든다"보다 "ICMP Echo Request/Reply를 raw socket 위에서 어디까지 직접 책임지는가"라는 질문으로 다시 읽는다. 현재 구현은 checksum 계산, packet build, IP header length를 고려한 reply parse, RTT 통계까지 직접 맡고, deterministic test는 fake raw socket으로 이를 고정한다. 따라서 이 lab의 핵심은 결과 문자열보다 binary packet contract와 권한 경계를 함께 다루는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/icmp_pinger.py`
- 테스트 근거: `python/tests/test_icmp_pinger.py`, `problem/Makefile`, `problem/script/test_icmp.sh`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 보조 실행: `python3 python/src/icmp_pinger.py example.com -c 1` 시도

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 결과: `11 passed in 0.01s`
- 보조 실행: live `example.com` probe는 현재 세션에서 5초 안에 완료되지 않았다
- live harness 참고: `make test-live`는 canonical test가 아니라 root 권한과 외부 네트워크를 전제로 둔 보조 검증 경로다

## 지금 남기는 한계

- IPv6/ICMPv6는 지원하지 않는다.
- live raw-socket path는 현재 네트워크와 OS 정책에 따라 재현성이 흔들린다.
- 시스템 `ping` 수준의 detailed summary나 duplicate detection은 넣지 않았다.
