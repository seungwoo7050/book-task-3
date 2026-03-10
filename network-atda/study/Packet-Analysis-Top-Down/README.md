# Packet Analysis Top-Down

HTTP에서 TLS까지 내려가며 Wireshark trace를 문제-증거-해설 구조로 읽는 패킷 분석 트랙입니다.

## 이 트랙이 맡는 역할

교재의 top-down 흐름을 따라가되, 정답 파일을 바로 던지는 대신 trace 범위, 관찰 가능한 근거, 개념 문서를 분리해 학습 가이드처럼 읽히도록 정리했습니다.

## 추천 선수 지식

- Wireshark 기본 화면과 display filter 사용법
- 프로토콜 필드명을 영어 원문으로 읽는 데 거부감이 없으면 좋습니다.
- 정답보다 근거를 먼저 확인하려는 태도가 중요합니다.

## 권장 프로젝트 순서

1. [HTTP Packet Analysis](http/README.md) - `verified`
   텍스트 기반 HTTP 요청/응답부터 시작해 Wireshark 분석 습관을 잡습니다.
2. [DNS Packet Analysis](dns/README.md) - `verified`
   이름 해석, record type, TTL 기반 캐시를 trace로 읽습니다.
3. [TCP and UDP Packet Analysis](tcp-udp/README.md) - `verified`
   TCP의 상태와 UDP의 단순성을 같은 시야에서 비교합니다.
4. [IP and ICMP Packet Analysis](ip-icmp/README.md) - `verified`
   IPv4 header, TTL, fragmentation, ICMP 메시지를 읽습니다.
5. [Ethernet and ARP Packet Analysis](ethernet-arp/README.md) - `verified`
   링크 계층 주소 해석과 ARP 교환을 확인합니다.
6. [802.11 Wireless Packet Analysis](wireless-802.11/README.md) - `verified`
   무선 LAN의 관리 프레임과 주소 체계를 읽습니다.
7. [TLS Packet Analysis](tls-ssl/README.md) - `verified`
   TLS handshake와 암호화 이후의 가시성 한계를 정리합니다.

## 공통 읽기 방법

- `problem/README.md`에서 질문 목록과 trace 범위를 먼저 확인합니다.
- `analysis/README.md`에서 공개 답안이 어떤 증거 원칙으로 작성되는지 읽습니다.
- `docs/README.md`에서 개념 문서를 골라 필요한 부분만 복습합니다.
- 이 트랙은 현재 `problem/`, `analysis/`, `docs/` 세 축으로 읽으면 충분합니다.

## 포트폴리오로 확장하기

- packet/frame 번호를 근거로 주장하는 습관을 보여 주면, 단순 요약보다 훨씬 신뢰도가 높습니다.
- Wireshark 필터, 캡처 화면, 해석 메모를 함께 묶어 두면 학습 레포가 포트폴리오형 네트워크 분석 노트로 발전합니다.
- 교재 trace만 반복하지 말고, 비슷한 질문을 새 trace에 다시 적용해 본 결과를 추가하면 차별화가 됩니다.

## 트랙 검증

- 전체 trace 점검: `make -C study/Packet-Analysis-Top-Down check-traces`
- 전체 답안 검증: `make -C study/Packet-Analysis-Top-Down test`
