# TCP and UDP Packet Analysis structure guide

## 이 글의 중심 질문

- TCP와 UDP의 차이를 실제 세그먼트와 datagram 증거로 어떻게 읽었는가?
- 한 줄 답: TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. handshake와 data segment를 비교 가능한 근거로 정리하기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`
- `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 `## Part 2: TCP Connection Management`
- `study/03-Packet-Analysis-Top-Down/tcp-udp/analysis/src/tcp-udp-analysis.md`의 `## Part 3: UDP`

## 리라이트 주의점

- `TCP and UDP Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
