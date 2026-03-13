# Traceroute structure guide

## 이 글의 중심 질문

- UDP probe와 ICMP 응답을 엮어 hop 단위 경로를 어떻게 복원했는가?
- 한 줄 답: TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.

## 권장 흐름

1. 실행 표면과 entrypoint를 먼저 고정하기
2. probe port 계산, ICMP 파싱, hop formatting을 한 경로로 묶기
3. 테스트와 남은 범위를 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`
- `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`의 `def trace_route`
- `study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`의 `def test_trace_route_returns_hops_until_destination`

## 리라이트 주의점

- `Traceroute`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 IPv6 traceroute는 지원하지 않습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
