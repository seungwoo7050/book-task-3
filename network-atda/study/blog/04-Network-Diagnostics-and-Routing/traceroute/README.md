# Traceroute Blog

이 문서 묶음은 `traceroute`를 "경로를 찍는 도구"보다 "TTL-limited UDP probe와 ICMP reply를 어떻게 서로 맞춰 hop line으로 바꾸는가"라는 질문으로 다시 읽는다. 현재 구현은 probe마다 고유 UDP dest port를 만들고, ICMP response 안의 embedded UDP header에서 그 port를 다시 꺼내 probe와 reply를 매칭한다. 따라서 이 lab의 핵심은 출력 형식보다 correlation rule과 termination rule을 명확히 세우는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/04-Network-Diagnostics-and-Routing/traceroute/problem/README.md`
- 구현 경계: `README.md`, `python/README.md`, `python/src/traceroute.py`
- 테스트 근거: `python/tests/test_traceroute.py`, `problem/Makefile`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- 보조 실행: `python3 python/src/traceroute.py example.com --max-hops 2 --probes 1 --timeout 0.2` 시도

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- 결과: `4 passed in 0.01s`
- 보조 실행: live `example.com` run은 현재 세션에서 5초 안에 완료되지 않았다
- 검증 구조 주의: problem spec이 명시하듯 canonical test는 raw socket 없이 parser/formatter를 확인하는 경로이고, live probing은 수동 재현 경로다

## 지금 남기는 한계

- IPv6 traceroute와 reverse DNS lookup은 지원하지 않는다.
- 현재 live path는 network environment에 크게 의존한다.
- ECMP, asymmetric routing, rate limiting 같은 internet-scale variability는 모델링하지 않는다.
