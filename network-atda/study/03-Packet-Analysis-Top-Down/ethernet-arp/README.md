# Ethernet and ARP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: 네트워크 계층 랩 다음에 링크 계층 주소 해석을 보며, 상위 계층 IP 주소와 하위 계층 MAC 주소가 어떻게 연결되는지 확인하게 합니다.

## 제공된 자료
- `problem/data/ethernet-arp.pcapng`: Ethernet/ARP trace
- `analysis/src/ethernet-arp-analysis.md`: 공개 답안
- `docs/concepts/arp-protocol.md`: ARP 개념 문서

## 이 레포의 답
- 한 줄 답: 링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/03-Packet-Analysis-Top-Down/ethernet-arp/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/03-Packet-Analysis-Top-Down/ethernet-arp/README.md` - 소스 기준의 분석 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- EtherType와 상위 프로토콜 연결
- ARP request broadcast / reply unicast
- 게이트웨이 MAC 해석
- ARP 보안 취약점의 기본 개념

## 현재 한계
- trace가 작아 교재의 일부 확장 질문은 관찰 불가입니다.
- Gratuitous ARP나 ARP spoofing 사례는 포함하지 않습니다.
