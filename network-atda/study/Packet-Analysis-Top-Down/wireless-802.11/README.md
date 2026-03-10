# 802.11 Wireless Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test` |

## 한 줄 요약

비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩입니다.

## 왜 이 프로젝트가 필요한가

Ethernet/ARP 다음에 무선 링크 계층의 차이를 관찰하며, 같은 링크 계층이라도 프레임 구조와 주소 의미가 크게 달라짐을 보여 줍니다.

## 이런 학습자에게 맞습니다

- 무선 LAN의 management frame을 Wireshark로 읽어 보고 싶은 학습자
- To DS/From DS 비트와 여러 MAC 주소 field의 의미를 이해하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/wireless-trace.pcap`: 802.11 monitor mode trace
- `analysis/src/wireless-analysis.md`: 공개 답안
- `docs/concepts/802.11-frame-format.md`: 802.11 프레임 개념 문서

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- management/control/data frame 분류
- beacon과 probe의 의미
- authentication -> association 절차
- `To DS`/`From DS`와 주소 field 해석

## 현재 한계

- compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있습니다.
- EAPOL/WPA handshake 심화는 포함하지 않습니다.
- 실제 RF 잡음과 retry 패턴은 제한적으로만 보입니다.

## 포트폴리오로 확장하기

- 관리 프레임 흐름을 타임라인 그림으로 정리하면 문서 친절도가 크게 올라갑니다.
- 무선과 유선 Ethernet의 차이를 표로 비교하면 저장소 전체의 학습 흐름이 잘 드러납니다.
- 직접 캡처한 trace와 비교 분석을 추가하면 차별화가 큽니다.
