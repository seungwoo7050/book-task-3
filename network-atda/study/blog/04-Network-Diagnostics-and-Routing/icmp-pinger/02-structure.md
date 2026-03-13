# ICMP Pinger structure guide

## 이 글의 중심 질문

- ICMP echo request/reply를 raw socket 위에서 어디까지 직접 조립하고 해석했는가?
- 한 줄 답: Raw socket으로 `ICMP Echo Request/Reply`를 직접 구현하는 진단 도구 과제입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. checksum, packet build, reply parse를 ping 흐름으로 연결하기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/src/icmp_pinger.py`의 `def ping`
- `study/04-Network-Diagnostics-and-Routing/icmp-pinger/python/tests/test_icmp_pinger.py`의 `def test_ping_prints_successful_reply_and_loss_stats`

## 리라이트 주의점

- `ICMP Pinger`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 IPv6/ICMPv6는 지원하지 않습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
