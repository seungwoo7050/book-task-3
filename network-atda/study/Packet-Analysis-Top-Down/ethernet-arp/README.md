# Ethernet and ARP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/ethernet-arp` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test` |

## 한 줄 요약

링크 계층 프레임과 IP-MAC 주소 해석 과정을 ARP request/reply 쌍으로 읽는 랩이다.

## 문제 요약

Ethernet header의 destination/source MAC, EtherType, broadcast/unicast 구분과 ARP request/reply를 분석한다.

## 이 프로젝트를 여기 둔 이유

네트워크 계층 랩 다음에 링크 계층 주소 해석을 보며, 상위 계층 IP 주소와 하위 계층 MAC 주소가 어떻게 연결되는지 확인한다.

## 제공 자료

- `problem/data/ethernet-arp.pcapng`
- `analysis/src/ethernet-arp-analysis.md`
- `docs/concepts/arp-protocol.md`

## 학습 포인트

- EtherType와 상위 프로토콜 연결
- ARP request broadcast / reply unicast
- 게이트웨이 MAC 해석
- ARP 보안 취약점 개념

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

trace가 매우 작아서 HTTP packet offset 같은 일부 교재 문항은 관찰 불가다.

- 현재 한계: Gratuitous ARP나 ARP spoofing 사례 trace는 없음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
