# IP and ICMP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/ip-icmp` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test` |

## 한 줄 요약

IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩이다.

## 문제 요약

ICMP Echo와 Time Exceeded, IPv4 fragmentation field, TTL 변화, traceroute hop 응답을 제공된 trace에서 분석한다.

## 이 프로젝트를 여기 둔 이유

transport 랩 다음에 네트워크 계층 헤더와 제어 메시지를 직접 읽으며, 이후 ICMP/traceroute 구현 프로젝트와 맞물린다.

## 제공 자료

- `problem/data/ip-traceroute.pcapng`
- `problem/data/ip-fragmentation.pcapng`
- `analysis/src/ip-icmp-analysis.md`

## 학습 포인트

- IPv4 header field 해석
- fragmentation 3요소(ID/flags/offset)
- TTL과 traceroute 관계
- ICMP type/code 구분

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

IPv4 중심이며, IPv6 비교는 개념 문서에만 있다.

- 현재 한계: IPv6 ICMPv6 실습 없음
- 현재 한계: OS별 traceroute 구현 차이까지 실험하진 않음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
