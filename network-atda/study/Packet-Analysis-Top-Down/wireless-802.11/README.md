# 802.11 Wireless Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/wireless-802.11` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test` |

## 한 줄 요약

비콘, 프로브, 인증, 연관, 주소 필드를 통해 무선 LAN 연결 과정을 읽는 랩이다.

## 문제 요약

802.11 management/control/data frame과 To DS/From DS 비트, beacon 정보, 인증과 연관 절차를 trace에서 분석한다.

## 이 프로젝트를 여기 둔 이유

Ethernet/ARP 랩 다음에 무선 링크 계층의 차이를 관찰해, 같은 링크 계층이라도 프레임 구조와 주소 의미가 크게 달라진다는 점을 보여준다.

## 제공 자료

- `problem/data/wireless-trace.pcap`
- `analysis/src/wireless-analysis.md`
- `docs/concepts/802.11-frame-format.md`

## 학습 포인트

- management/control/data frame 분류
- beacon과 probe 의미
- authentication -> association 절차
- To DS/From DS와 주소 필드 해석

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

compact synthetic trace라 실제 monitor-mode 캡처보다 단순화된 부분이 있다.

- 현재 한계: EAPOL/WPA handshake 심화 없음
- 현재 한계: 실제 RF 환경 잡음과 retry 패턴은 제한적

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
