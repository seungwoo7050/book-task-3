# IP and ICMP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 IP/ICMP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test` |

## 한 줄 요약

IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩입니다.

## 왜 이 프로젝트가 필요한가

전송 계층 랩 다음에 네트워크 계층 헤더와 제어 메시지를 직접 읽으며, 이후 `ICMP Pinger`와 `Traceroute` 구현 프로젝트와 맞물리게 합니다.

## 이런 학습자에게 맞습니다

- IPv4 header와 ICMP type/code를 trace에서 직접 읽고 싶은 학습자
- fragmentation과 TTL 개념을 실습 근거와 함께 정리하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/ip-traceroute.pcapng`: traceroute 관련 IP/ICMP trace
- `problem/data/ip-fragmentation.pcapng`: fragmentation이 일어난 ICMP trace
- `analysis/src/ip-icmp-analysis.md`: 공개 답안

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- IPv4 header field 해석
- fragmentation 3요소(`Identification`, `Flags`, `Offset`)
- TTL과 traceroute 관계
- ICMP type/code 구분

## 현재 한계

- IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다.
- OS별 traceroute 구현 차이는 실험하지 않습니다.

## 포트폴리오로 확장하기

- fragmentation 계산 과정을 표나 그림으로 정리하면 이해가 훨씬 쉬워집니다.
- `ICMP Pinger`, `Traceroute` 구현 프로젝트와 교차 링크를 걸면 저장소 전체 흐름이 좋아집니다.
- 실제 traceroute 출력과 trace를 대응시킨 보조 메모를 추가하면 차별화가 됩니다.
