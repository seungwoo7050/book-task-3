# UDP Pinger Blog

이 문서 묶음은 `udp-pinger`를 "ping을 찍는다"보다 "연결 없는 전송에서 애플리케이션이 timeout과 손실 통계를 직접 떠안는가"라는 질문으로 다시 읽는다. 현재 구현은 10개의 datagram을 보내고, 1초 timeout을 손실 판정으로 바꾸며, 마지막에 min/avg/max RTT와 loss percentage를 계산한다.

이번 재작성은 기존 blog 본문이 아니라 `problem/README.md`, `python/README.md`, `python/src/udp_pinger_client.py`, `python/tests/test_udp_pinger.py`, 그리고 2026-03-14 재실행한 `make -C .../problem test`만 사용했다.

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증: `make -C network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`
- 결과: 10개 ping 중 8개 응답, `20.0% loss`, `RTT min/avg/max = 0.053/0.156/0.472 ms`, 테스트 `3 passed`

## 지금 남기는 한계

- 순서 역전 별도 처리 없음
- 분위수 같은 고급 통계 없음
- 단독 `pytest`는 제공 서버 선기동 필요
