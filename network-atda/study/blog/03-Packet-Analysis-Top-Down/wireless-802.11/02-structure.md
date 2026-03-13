# 802.11 Wireless Packet Analysis structure guide

## 이 글의 중심 질문

- 무선 링크 계층에서는 beacon, probe, association이 어떤 순서로 보이는가?
- 한 줄 답: 비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. beacon과 probe 이후 association 흐름을 이어 읽기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`
- `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 `## Part 2: Probe Request and Response (Q6–Q9)`
- `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`의 `## Part 3: Authentication and Association (Q10–Q14)`

## 리라이트 주의점

- `802.11 Wireless Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
