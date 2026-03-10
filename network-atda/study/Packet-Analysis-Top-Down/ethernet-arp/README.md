# Ethernet and ARP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test` |

## 한 줄 요약

링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩입니다.

## 왜 이 프로젝트가 필요한가

네트워크 계층 랩 다음에 링크 계층 주소 해석을 보며, 상위 계층 IP 주소와 하위 계층 MAC 주소가 어떻게 연결되는지 확인하게 합니다.

## 이런 학습자에게 맞습니다

- Ethernet header, EtherType, ARP opcode를 trace에서 직접 읽고 싶은 학습자
- IP 주소와 MAC 주소의 연결이 trace에 어떻게 드러나는지 보고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/ethernet-arp.pcapng`: Ethernet/ARP trace
- `analysis/src/ethernet-arp-analysis.md`: 공개 답안
- `docs/concepts/arp-protocol.md`: ARP 개념 문서

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- EtherType와 상위 프로토콜 연결
- ARP request broadcast / reply unicast
- 게이트웨이 MAC 해석
- ARP 보안 취약점의 기본 개념

## 현재 한계

- trace가 작아 교재의 일부 확장 질문은 관찰 불가입니다.
- Gratuitous ARP나 ARP spoofing 사례는 포함하지 않습니다.

## 포트폴리오로 확장하기

- Ethernet과 ARP를 그림으로 풀어 쓴 도식 한 장만 추가해도 문서 친절도가 크게 좋아집니다.
- 게이트웨이 MAC을 실제 네트워크 구성과 연결한 메모를 남기면 실전 감각이 드러납니다.
- ARP spoofing 방어 관점까지 연결하면 보안 학습 흔적도 함께 보여 줄 수 있습니다.
