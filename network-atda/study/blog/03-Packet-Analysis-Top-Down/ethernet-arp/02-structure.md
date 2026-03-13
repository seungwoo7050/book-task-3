# Ethernet and ARP Packet Analysis structure guide

## 이 글의 중심 질문

- Ethernet frame과 ARP 교환을 링크 계층 주소 관점에서 어떻게 읽었는가?
- 한 줄 답: 링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. MAC 주소와 ARP 질의/응답을 한 시야로 붙들기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`
- `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`의 `## Part 2: ARP Protocol`
- `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`의 `## Part 3: Broadcast and Caching`

## 리라이트 주의점

- `Ethernet and ARP Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 trace가 작아 교재의 일부 확장 질문은 관찰 불가입니다. 같은 남은 경계를 사람 말로 다시 정리한다.
