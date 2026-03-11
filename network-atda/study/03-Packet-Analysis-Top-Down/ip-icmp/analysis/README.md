# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `IP and ICMP Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/ip-icmp-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`

## 현재 범위
IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩입니다.

## 남은 약점
- IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다.
- OS별 traceroute 구현 차이는 실험하지 않습니다.
