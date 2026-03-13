# IP and ICMP Packet Analysis structure guide

## 이 글의 중심 질문

- IP header, fragmentation, ICMP 메시지를 trace 안에서 어디까지 설명할 수 있는가?
- 한 줄 답: IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. IPv4 header와 ICMP 흐름을 같은 분석 축으로 묶기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`
- `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`의 `## Part 2: IP Fragmentation`
- `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`의 `## Part 3: ICMP and Traceroute`

## 리라이트 주의점

- `IP and ICMP Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다. 같은 남은 경계를 사람 말로 다시 정리한다.
