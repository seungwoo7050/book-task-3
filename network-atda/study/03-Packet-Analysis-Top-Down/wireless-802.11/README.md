# 802.11 Wireless Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: Ethernet/ARP 다음에 무선 링크 계층의 차이를 관찰하며, 같은 링크 계층이라도 프레임 구조와 주소 의미가 크게 달라짐을 보여 줍니다.

## 제공된 자료
- `problem/data/wireless-trace.pcap`: 802.11 monitor mode trace
- `analysis/src/wireless-analysis.md`: 공개 답안
- `docs/concepts/802.11-frame-format.md`: 802.11 프레임 개념 문서

## 이 레포의 답
- 한 줄 답: 비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- management/control/data frame 분류
- beacon과 probe의 의미
- authentication -> association 절차
- `To DS`/`From DS`와 주소 field 해석

## 현재 한계
- compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- EAPOL/WPA handshake 심화는 포함하지 않습니다.
- 실제 RF 잡음과 retry 패턴은 제한적으로만 보입니다.
